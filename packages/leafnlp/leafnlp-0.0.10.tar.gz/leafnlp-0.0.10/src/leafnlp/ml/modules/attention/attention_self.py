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


class AttentionSelf(torch.nn.Module):

    def __init__(self,
                 input_size: int,
                 hidden_size: int,
                 dropout_rate: float = None,
                 device=torch.device("cpu")):
        """implementation of self-attention.

        Args:
            * ``input_size`` (**int**): size of input.
            * ``hidden_size`` (**int**): size of hidden states.
            * ``dropout_rate`` (**float**, optional): dropout rate. Defaults to None.
            * ``device`` (_type_, optional): Device. Defaults to torch.device("cpu").
        """

        super().__init__()
        self.dropout_rate = dropout_rate
        self.device = device

        self.ff1 = torch.nn.Linear(input_size, hidden_size)
        self.ff2 = torch.nn.Linear(hidden_size, 1, bias=False)
        if dropout_rate is not None:
            self.model_drop = torch.nn.Dropout(dropout_rate)

    def forward(self, input_, mask=None):
        """_summary_

        Args:
            * ``input_`` (_type_): _description_
            * ``mask`` (_type_, optional): _description_. Defaults to None.

        Returns:
            * ``attn_``: attention weights
            * ``ctx_vec``: context vector
        """        

        attn_ = torch.tanh(self.ff1(input_))
        attn_ = self.ff2(attn_).squeeze(2)
        if mask is not None:
            attn_ = attn_.masked_fill(mask == 0, -1e9)
        # dropout method 1.
        # if self.dropout_rate is not None:
        #     drop_mask = Variable(torch.ones(attn_.size())).to(self.device)
        #     drop_mask = self.model_drop(drop_mask)
        #     attn_ = attn_.masked_fill(drop_mask == 0, -1e9)

        attn_ = torch.softmax(attn_, dim=1)
        # dropout method 2.
        if self.dropout_rate is not None:
            attn_ = self.model_drop(attn_)
        ctx_vec = torch.bmm(attn_.unsqueeze(1), input_).squeeze(1)

        return attn_, ctx_vec
