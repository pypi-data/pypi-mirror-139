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


class CrossAttention(torch.nn.Module):
    """Implement of Co-attention.

    Args:
        torch (_type_): _description_

    Returns:
        _type_: _description_
    """    

    def __init__(self):
        super().__init__()

    def forward(self, inputA, inputB, maskA=None, maskB=None):
        """_summary_

        Args:
            * ``inputA`` (_type_): _description_
            * ``inputB`` (_type_): _description_
            * ``maskA`` (_type_, optional): _description_. Defaults to None.
            * ``maskB`` (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        

        assert inputA.size(-1) == inputB.size(-1)

        scores = torch.bmm(inputA, inputB.transpose(1, 2))
        if maskA is not None and maskB is not None:
            maskA = maskA[:, :, None]
            maskB = maskB[:, None, :]
            mask = torch.bmm(maskA, maskB)
            scores = scores.masked_fill(mask == 0, -1e10)

        attnA = torch.softmax(scores, 1)
        attnB = torch.softmax(scores, 2)
        cvA = torch.bmm(attnA.transpose(1, 2), inputA)
        cvB = torch.bmm(attnB, inputB)

        return (attnA, cvA), (attnB, cvB)
