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

from leafnlp.ml.modules.embedding.position_embedding import PositionalEmbedding


class BertEmbeddings(torch.nn.Module):
    """Implementation of BERT embedding layer.
    Not follow the original implementation.

    Args:
        torch (_type_): _description_

    Returns:
        _type_: _description_
    """

    def __init__(self, vocab_size, hidden_size,
                 drop_rate, device=torch.device("cpu")):
        super().__init__()

        self.device = device

        self.word_embeddings = torch.nn.Embedding(
            vocab_size, hidden_size).to(device)
        self.segment_embeddings = torch.nn.Embedding(
            2, hidden_size).to(device)
        self.position_embeddings = PositionalEmbedding(
            hidden_size, device).to(device)

        self.proj2vocab = torch.nn.Linear(
            hidden_size, vocab_size).to(device)
        self.proj2vocab.weight.data = self.word_embeddings.weight.data

        self.dropout = torch.nn.Dropout(drop_rate).to(device)

    def forward(self, input_tokens, input_seg=None):
        """_summary_

        Args:
            input_tokens (_type_): input sequence token ids.
            input_seg (_type_, optional): input segment ids.. Defaults to None.

        Returns:
            _type_: _description_
        """

        word_vec = self.word_embeddings(input_tokens)
        position_vec = self.position_embeddings(input_tokens)
        if input_seg is None:
            input_seg = torch.zeros(
                input_tokens.size(), dtype=torch.long).to(self.device)

        seg_vec = self.segment_embeddings(input_seg)
        output_vec = word_vec + position_vec + seg_vec
        output_vec = self.dropout(output_vec)

        return output_vec

    def get_word_embedding(self, input_tokens):
        """Get word embedding only.

        Args:
            * ``input_tokens`` (_type_): _description_

        Returns:
            _type_: _description_
        """

        return self.word_embeddings(input_tokens)

    def get_vec2vocab(self, input_data):
        """_summary_

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """

        return self.proj2vocab(input_data)
