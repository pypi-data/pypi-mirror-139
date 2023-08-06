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

import numpy as np
import torch
from leafnlp.ml.modules.attention.attention_multi_head import \
    MultiHeadedAttention_Basic
from leafnlp.ml.modules.utils.LayerNormalization import LayerNormalization
from leafnlp.ml.modules.utils.PositionwiseFeedForward import \
    PositionwiseFeedForward_Basic
from torch.autograd import Variable


class TransformerLayer(torch.nn.Module):
    """Implementation of Transformer Decoder Layer.

    Args:
        torch (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, input_size,
                 n_heads, drop_rate,
                 device=torch.device("cpu")):
        super().__init__()
        # multi-head attention
        self.attnSelf = MultiHeadedAttention_Basic(
            n_heads, input_size, drop_rate).to(device)
        self.attnEnc = MultiHeadedAttention_Basic(
            n_heads, input_size, drop_rate).to(device)
        # layer normalization
        self.norm1 = LayerNormalization(input_size).to(device)
        self.norm2 = LayerNormalization(input_size).to(device)
        self.norm3 = LayerNormalization(input_size).to(device)
        # layer feed-forward
        self.pos_ff = PositionwiseFeedForward_Basic(
            input_size, input_size*4, input_size, drop_rate
        ).to(device)

        self.drop = torch.nn.Dropout(drop_rate).to(device)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        """Transformer Layer

        Args:
            * ``src`` (_type_): _description_
            * ``tgt`` (_type_): _description_
            * ``src_mask`` (_type_, optional): _description_. Defaults to None.
            * ``tgt_mask`` (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        

        tgt = self.norm1(
            tgt + self.drop(self.attnSelf(tgt, tgt, tgt, tgt_mask)))
        tgt = self.norm2(
            tgt + self.drop(self.attnEnc(tgt, src, src, src_mask)))
        tgt = self.norm2(tgt + self.pos_ff(tgt))

        return self.drop(tgt)


class TransformerDecoder(torch.nn.Module):
    """Implementation of Transformer Decoder

    Args:
        torch (_type_): _description_

    Returns:
        _type_: _description_
    """    

    def __init__(self, input_size, n_heads, n_layers,
                 drop_rate, device=torch.device("cpu")):
        super().__init__()
        self.n_heads = n_heads
        self.device = device
        self.n_layers = n_layers

        self.tf_layers = torch.nn.ModuleList(
            [TransformerLayer(input_size, n_heads, drop_rate, device)
             for k in range(n_layers)]).to(device)

    def forward(self, src, tgt, src_mask=None):
        """_summary_

        Args:
            * ``src`` (_type_): _description_
            * ``tgt`` (_type_): _description_
            * ``src_mask`` (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        

        batch_size = tgt.size(0)
        seq_len = tgt.size(1)
        mask_ = 1-np.triu(np.ones([seq_len, seq_len]), k=1)
        tgt_mask = Variable(torch.LongTensor(mask_)).to(self.device)
        tgt_mask = tgt_mask.unsqueeze(0).unsqueeze(
            0).expand(batch_size, self.n_heads, -1, -1)

        if src_mask is not None:
            src_mask = src_mask.unsqueeze(1).unsqueeze(1)

        tgt = self.tf_layers[0](src, tgt, src_mask, tgt_mask)
        for k in range(1, self.n_layers):
            tgt = self.tf_layers[k](src, tgt, src_mask, tgt_mask)

        return tgt
