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
from leafnlp.ml.modules.attention.attention_multi_head import \
    MultiHeadedAttention_Basic
from leafnlp.ml.modules.utils.LayerNormalization import LayerNormalization
from leafnlp.ml.modules.utils.PositionwiseFeedForward import \
    PositionwiseFeedForward_Basic


class TransformerLayer(torch.nn.Module):
    """Implementation of Transformer

    Args:
        * ``input_size`` (**int**, optional): _description_. Defaults to 768.
        * ``n_heads`` (**int**, optional): _description_. Defaults to 12.
        * ``drop_rate`` (**float**, optional): _description_. Defaults to 0.2.
        * ``device`` (_type_, optional): _description_. Defaults to torch.device("cpu").
    """

    def __init__(self,
                 input_size: int = 768,
                 n_heads: int = 12,
                 drop_rate: float = 0.2,
                 device=torch.device("cpu")):

        super().__init__()
        # multi-head attention
        self.attentionMH = MultiHeadedAttention_Basic(
            n_heads, input_size, drop_rate).to(device)
        # layer normalization
        self.norm = LayerNormalization(input_size).to(device)
        # layer feed-forward
        self.pos_ff = PositionwiseFeedForward_Basic(
            input_size, input_size*4, input_size, drop_rate
        ).to(device)
        self.drop = torch.nn.Dropout(drop_rate).to(device)

    def forward(self, input_data, mask=None):
        """Transformer Layer

        Args:
            * ``input_data`` (_type_): _description_
            * ``mask`` (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """

        if mask is not None:
            mask = mask.unsqueeze(1).unsqueeze(1)
        hidden = self.attentionMH(input_data, input_data, input_data, mask)
        hidden = self.norm(input_data + self.drop(hidden))
        hidden = self.norm(hidden + self.pos_ff(hidden))

        return self.drop(hidden)


class TransformerEncoder(torch.nn.Module):
    """Implementation of Transformer Encoder

    Args:
        * ``input_size`` (**int**, optional): _description_. Defaults to 768.
        * ``n_heads`` (**int**, optional): _description_. Defaults to 12.
        * ``n_layers`` (**int**, optional): _description_. Defaults to 12.
        * ``drop_rate`` (**float**, optional): _description_. Defaults to 0.1.
        * ``device`` (_type_, optional): _description_. Defaults to torch.device("cpu").
    """

    def __init__(self,
                 input_size: int = 768,
                 n_heads: int = 12,
                 n_layers: int = 12,
                 drop_rate: float = 0.1,
                 device=torch.device("cpu")):
        super().__init__()

        self.n_layers = n_layers

        self.tf_layers = torch.nn.ModuleList(
            [TransformerLayer(input_size, n_heads, drop_rate, device)
             for k in range(n_layers)]).to(device)

    def forward(self, input_data, mask=None):
        """_summary_

        Args:
            * ``input_data`` (_type_): _description_
            * ``mask`` (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """

        output = []
        out = self.tf_layers[0](input_data, mask)
        output.append(out)
        for k in range(1, self.n_layers):
            out = self.tf_layers[k](out, mask)
            output.append(out)

        return output
