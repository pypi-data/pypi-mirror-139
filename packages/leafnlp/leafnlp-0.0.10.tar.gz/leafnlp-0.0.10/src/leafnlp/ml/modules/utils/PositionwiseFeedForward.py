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
from leafnlp.ml.modules.activation.functions import gelu


class PositionwiseFeedForward_Basic(torch.nn.Module):
    """Implementation of Positionwise FeedForward Network.

    Args:
        * ``input_size`` (**int**): input size
        * ``hidden_size`` (**int**): hidden size
        * ``output_size`` (**int**): output size
        * ``drop_rate`` (**float**): dropout rate
    """        

    def __init__(self, 
                 input_size: int,
                 hidden_size: int, 
                 output_size: int, 
                 drop_rate: float):
        super().__init__()

        self.ff1 = torch.nn.Linear(input_size, hidden_size)
        self.ff2 = torch.nn.Linear(hidden_size, output_size)
        self.drop = torch.nn.Dropout(drop_rate, inplace=True)

    def forward(self, input_):

        output = self.drop(gelu(self.ff1(input_)))
        output = self.drop(self.ff2(output))

        return output
