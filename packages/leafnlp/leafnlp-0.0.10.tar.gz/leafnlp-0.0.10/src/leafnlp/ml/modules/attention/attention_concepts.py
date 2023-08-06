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


class Attention_Concepts(torch.nn.Module):

    def __init__(self, 
                 input_size: int, 
                 n_concepts: int,
                 device=torch.device("cpu")):
        """implementation of self-attention.

        Args:
            * ``input_size`` (**int**): input size.
            * ``n_concepts`` (**int**): number of concepts.
            * ``device`` (_type_, optional): Defaults to torch.device("cpu").
        """        

        super().__init__()
        self.n_concepts = n_concepts

        self.ff = torch.nn.ModuleList([
            torch.nn.Linear(input_size, 1, bias=False)
            for k in range(n_concepts)]).to(device)

    def forward(self, input_, mask=None):
        """_summary_

        Args:
            * ``input_`` (_type_): _description_
            * ``mask`` (_type_, optional): _description_. Defaults to None.

        Returns:
            * ``attn_weights``: attention weights
            * ``attn_ctx_vec``: context vector
        """        

        batch_size = input_.size(0)

        attn_weight = []
        attn_ctx_vec = []
        for k in range(self.n_concepts):
            attn_ = self.ff[k](input_).squeeze(2)
            if mask is not None:
                attn_ = attn_.masked_fill(mask == 0, -1e9)
            attn_ = torch.softmax(attn_, dim=1)
            ctx_vec = torch.bmm(attn_.unsqueeze(1), input_).squeeze(1)
            attn_weight.append(attn_)
            attn_ctx_vec.append(ctx_vec)

        attn_weight = torch.cat(attn_weight, 0).view(
            self.n_concepts, batch_size, -1)
        attn_weight = attn_weight.transpose(0, 1)
        attn_ctx_vec = torch.cat(attn_ctx_vec, 0).view(
            self.n_concepts, batch_size, -1)
        attn_ctx_vec = attn_ctx_vec.transpose(0, 1)

        return attn_weight, attn_ctx_vec
