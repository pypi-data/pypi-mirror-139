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
from torch.autograd import Variable


class EncoderRNN(torch.nn.Module):
    """RNN encoder

    Args:
        * ``emb_dim`` (**int**, optional): _description_. Defaults to 256.
        * ``hidden_size`` (**int**, optional): _description_. Defaults to 256.
        * ``nLayers`` (**int**, optional): _description_. Defaults to 2.
        * ``rnn_network`` (**str**, optional): _description_. Defaults to "lstm".
        * ``bidirectional`` (**bool**, optional): _description_. Defaults to True.
        * ``device`` (_type_, optional): _description_. Defaults to torch.device("cpu").
    """

    def __init__(self,
                 emb_dim: int = 256,
                 hidden_size: int = 256,
                 nLayers: int = 2,
                 rnn_network: str = "lstm",
                 bidirectional: bool = True,
                 device=torch.device("cpu")):
        super().__init__()
        self.hidden_size = hidden_size
        self.rnn_network = rnn_network
        self.nLayers = nLayers
        self.device = device
        self.bidirectional = bidirectional

        if rnn_network == 'lstm':
            self.encoder = torch.nn.LSTM(
                input_size=emb_dim,
                hidden_size=hidden_size,
                num_layers=nLayers,
                batch_first=True,
                bidirectional=bidirectional
            ).to(device)
        elif rnn_network == 'gru':
            self.encoder = torch.nn.GRU(
                input_size=emb_dim,
                hidden_size=hidden_size,
                num_layers=nLayers,
                batch_first=True,
                bidirectional=bidirectional
            ).to(device)

    def forward(self, input_data):
        """get encoding

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """

        n_dk = 1
        if self.bidirectional:
            n_dk = 2
        batch_size = input_data.size(0)

        h0_encoder = Variable(torch.zeros(
            n_dk*self.nLayers, batch_size, self.hidden_size)).to(self.device)
        if self.rnn_network == 'lstm':
            c0_encoder = Variable(torch.zeros(
                n_dk*self.nLayers, batch_size, self.hidden_size)).to(self.device)
            # encoding
            hy_encoder, (ht_encoder, ct_encoder) = self.encoder(
                input_data, (h0_encoder, c0_encoder))

            return hy_encoder, (ht_encoder, ct_encoder)

        elif self.rnn_network == 'gru':
            # encoding
            hy_encoder, ht_encoder = self.encoder(input_data, h0_encoder)

            return hy_encoder, ht_encoder
