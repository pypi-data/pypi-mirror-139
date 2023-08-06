import math
from typing import Callable, List, Tuple

import torch
import torch.nn.functional as F
from torch.optim.optimizer import Optimizer

from pytorch_optimizer.gc import centralize_gradient
from pytorch_optimizer.types import BETAS, CLOSURE, DEFAULTS, LOSS, PARAMETERS


class AdamP(Optimizer):
    """
    Reference : https://github.com/clovaai/AdamP
    Example :
        from pytorch_optimizer import AdamP
        ...
        model = YourModel()
        optimizer = AdamP(model.parameters())
        ...
        for input, output in data:
          optimizer.zero_grad()
          loss = loss_function(output, model(input))
          loss.backward()
          optimizer.step()
    """

    def __init__(
        self,
        params: PARAMETERS,
        lr: float = 1e-3,
        betas: BETAS = (0.9, 0.999),
        weight_decay: float = 0.0,
        delta: float = 0.1,
        wd_ratio: float = 0.1,
        use_gc: bool = False,
        nesterov: bool = False,
        adamd_debias_term: bool = False,
        eps: float = 1e-8,
    ):
        """AdamP optimizer
        :param params: PARAMETERS. iterable of parameters to optimize or dicts defining parameter groups
        :param lr: float. learning rate
        :param betas: BETAS. coefficients used for computing running averages of gradient and the squared hessian trace
        :param weight_decay: float. weight decay (L2 penalty)
        :param delta: float. threshold that determines whether a set of parameters is scale invariant or not
        :param wd_ratio: float. relative weight decay applied on scale-invariant parameters compared to that applied
            on scale-variant parameters
        :param use_gc: bool. use gradient centralization
        :param nesterov: bool. enables Nesterov momentum
        :param adamd_debias_term: bool. Only correct the denominator to avoid inflating step sizes early in training
        :param eps: float. term added to the denominator to improve numerical stability
        """
        self.lr = lr
        self.betas = betas
        self.weight_decay = weight_decay
        self.eps = eps
        self.wd_ratio = wd_ratio
        self.use_gc = use_gc

        self.check_valid_parameters()

        defaults: DEFAULTS = dict(
            lr=lr,
            betas=betas,
            weight_decay=weight_decay,
            delta=delta,
            wd_ratio=wd_ratio,
            nesterov=nesterov,
            adamd_debias_term=adamd_debias_term,
            eps=eps,
        )
        super().__init__(params, defaults)

    def check_valid_parameters(self):
        if self.lr < 0.0:
            raise ValueError(f'Invalid learning rate : {self.lr}')
        if not 0.0 <= self.betas[0] < 1.0:
            raise ValueError(f'Invalid beta_0 : {self.betas[0]}')
        if not 0.0 <= self.betas[1] < 1.0:
            raise ValueError(f'Invalid beta_1 : {self.betas[1]}')
        if self.weight_decay < 0.0:
            raise ValueError(f'Invalid weight_decay : {self.weight_decay}')
        if self.eps < 0.0:
            raise ValueError(f'Invalid eps : {self.eps}')
        if not 0.0 <= self.wd_ratio < 1.0:
            raise ValueError(f'Invalid wd_ratio : {self.wd_ratio}')

    @staticmethod
    def channel_view(x: torch.Tensor) -> torch.Tensor:
        return x.view(x.size()[0], -1)

    @staticmethod
    def layer_view(x: torch.Tensor) -> torch.Tensor:
        return x.view(1, -1)

    @staticmethod
    def cosine_similarity(
        x: torch.Tensor,
        y: torch.Tensor,
        eps: float,
        view_func: Callable[[torch.Tensor], torch.Tensor],
    ) -> torch.Tensor:
        x = view_func(x)
        y = view_func(y)
        return F.cosine_similarity(x, y, dim=1, eps=eps).abs_()

    def projection(
        self,
        p,
        grad,
        perturb: torch.Tensor,
        delta: float,
        wd_ratio: float,
        eps: float,
    ) -> Tuple[torch.Tensor, float]:
        wd: float = 1.0
        expand_size: List[int] = [-1] + [1] * (len(p.shape) - 1)
        for view_func in (self.channel_view, self.layer_view):
            cosine_sim = self.cosine_similarity(grad, p, eps, view_func)

            if cosine_sim.max() < delta / math.sqrt(view_func(p).size()[1]):
                p_n = p / view_func(p).norm(dim=1).view(expand_size).add_(eps)
                perturb -= p_n * view_func(p_n * perturb).sum(dim=1).view(expand_size)
                wd = wd_ratio
                return perturb, wd

        return perturb, wd

    @torch.no_grad()
    def step(self, closure: CLOSURE = None) -> LOSS:
        loss: LOSS = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                if grad.is_sparse:
                    raise RuntimeError('AdamP does not support sparse gradients')

                state = self.state[p]
                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p)
                    state['exp_avg_sq'] = torch.zeros_like(p)

                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']

                state['step'] += 1
                beta1, beta2 = group['betas']

                bias_correction1 = 1.0 - beta1 ** state['step']
                bias_correction2 = 1.0 - beta2 ** state['step']

                if self.use_gc:
                    grad = centralize_gradient(grad, gc_conv_only=False)

                exp_avg.mul_(beta1).add_(grad, alpha=1.0 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1.0 - beta2)

                de_nom = (exp_avg_sq.sqrt() / math.sqrt(bias_correction2)).add_(group['eps'])

                if group['nesterov']:
                    perturb = (beta1 * exp_avg + (1.0 - beta1) * grad) / de_nom
                else:
                    perturb = exp_avg / de_nom

                wd_ratio: float = 1
                if len(p.shape) > 1:
                    perturb, wd_ratio = self.projection(
                        p,
                        grad,
                        perturb,
                        group['delta'],
                        group['wd_ratio'],
                        group['eps'],
                    )

                if group['weight_decay'] > 0:
                    p.mul_(1.0 - group['lr'] * group['weight_decay'] * wd_ratio)

                step_size = group['lr']
                if not group['adamd_debias_term']:
                    step_size /= bias_correction1

                p.add_(perturb, alpha=-step_size)

        return loss
