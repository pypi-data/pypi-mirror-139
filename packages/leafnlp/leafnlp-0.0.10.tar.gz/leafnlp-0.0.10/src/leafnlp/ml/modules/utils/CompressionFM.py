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


class CompressionFM(torch.nn.Module):
    """Factor Machine

    Args:
        * ``input_size`` (**int**): _description_
        * ``fm_size`` (**int**): _description_
    """

    def __init__(self,
                 input_size: int,
                 fm_size: int):
        super().__init__()
        self.LW = torch.nn.Linear(input_size, 1)
        self.QV = torch.nn.Parameter(
            torch.randn(input_size, fm_size))

    def forward(self, input_data):
        """Factor Machine Implementation.

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """
        size_input = input_data.size()
        input_data = input_data.contiguous().view(-1, input_data.size(-1))
        h0 = self.LW(input_data)
        v1 = torch.mm(input_data, self.QV)
        v1 = v1*v1
        v2 = torch.mm(input_data*input_data, self.QV*self.QV)
        vcat = torch.sum(v1 - v2, 1)

        fm = h0.squeeze() + 0.5*vcat
        fm = fm.view(size_input[0], size_input[1], 1)

        return fm
