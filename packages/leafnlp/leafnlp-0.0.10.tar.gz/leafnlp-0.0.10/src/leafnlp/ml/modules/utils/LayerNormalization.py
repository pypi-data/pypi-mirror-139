# Copyright 2021 The LeafNLP Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch


class LayerNormalization(torch.nn.Module):

    """Transformer Layer Normalization.

    Args:
        * ``size`` (**int**): _description_
        * ``eps`` (**float**, optional): _description_. Defaults to 1e-5.
        * ``bias`` (**bool**, optional): _description_. Defaults to False.
    """

    def __init__(self,
                 size: int,
                 eps: float = 1e-5,
                 bias: bool = False):

        super().__init__()

        self.eps = eps
        self.bias = bias

        self.gamma = torch.nn.Parameter(torch.ones(size))
        self.register_parameter('gamma', self.gamma)

        if bias:
            self.beta = torch.nn.Parameter(torch.zeros(size))
            self.register_parameter('beta', self.beta)

    def forward(self, input_data):
        """gamma * (input - mean) / (std + eps) + bias

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """        
        
        mean = torch.mean(input_data, -1, keepdim=True)
        std = torch.mean((input_data-mean)*(input_data-mean), -1, keepdim=True)

        output = self.gamma*(input_data-mean)/torch.sqrt(std + self.eps)
        if self.bias:
            output = output + self.beta

        return output
