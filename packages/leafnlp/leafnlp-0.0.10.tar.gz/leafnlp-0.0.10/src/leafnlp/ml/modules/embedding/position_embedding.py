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

import math

import torch


class PositionalEmbedding(torch.nn.Module):
    """Implementation of Positional Embedding.

    Args:
        torch (_type_): _description_

    Returns:
        _type_: _description_
    """    

    def __init__(self, hidden_size, device=torch.device("cpu")):
        super().__init__()
        self.hidden_size = hidden_size

        self.posEmb = torch.zeros(10000, hidden_size, dtype=torch.float)
        self.posEmb.require_grad = False

        position = torch.arange(10000, dtype=torch.float).unsqueeze(1)
        p_term1 = torch.arange(0, hidden_size, 2, dtype=torch.float)
        p_term2 = - math.log(10000.0) / hidden_size
        inv_term = torch.exp(p_term1 * p_term2)

        posEmb_input = position * inv_term
        self.posEmb[:, 0::2] = torch.sin(posEmb_input)
        self.posEmb[:, 1::2] = torch.cos(posEmb_input)

        self.posEmb = self.posEmb.unsqueeze(0).to(device)

    def forward(self, input_data):
        """_summary_

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """        

        seq_len = input_data.size(1)
        pos_emb = self.posEmb[:, :seq_len]

        return pos_emb
