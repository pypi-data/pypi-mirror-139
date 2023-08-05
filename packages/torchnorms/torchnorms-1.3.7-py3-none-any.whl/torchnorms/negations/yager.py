# -*- coding: utf-8 -*-

import torch
from typing import Optional
from torch import nn, Tensor
from torchnorms.negations.base import BaseNegation


class YagerNegation(BaseNegation):
	def __init__(self,
				 p: Optional[Tensor] = None,
				 default_p: float = 0.1) -> None:
		super().__init__()
		self.p = p
		if self.p is None:
			assert default_p > -1
			self.p = nn.Parameter(torch.tensor(default_p))
		assert len(self.p.shape) == 0

		self.relu = torch.nn.ReLU()

		self.eps = 0.01
		self.__name__ = 'Yager'

	def __call__(self, a: Tensor) -> Tensor:

		self.p.data = self.relu(self.p.data + 1) - 1

		if self.p == 0:
			self.p.data += self.eps
		res = torch.pow((1.0 - torch.pow(a, self.p)), 1.0 / self.p)
		
		return res
