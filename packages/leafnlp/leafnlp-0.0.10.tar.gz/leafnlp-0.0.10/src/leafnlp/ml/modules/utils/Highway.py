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


class HighwayFeedForward(torch.nn.Module):
    """Highway Network

    Args:
        * ``hidden_size`` (**int**, optional): hidden size. Defaults to 256.
        * ``drop_rate`` (**float**, optional): dropout rate. Defaults to 0.2.
    """

    def __init__(self,
                 hidden_size: int = 256,
                 drop_rate: float = 0.2):
        super(HighwayFeedForward, self).__init__()

        self.ff1 = torch.nn.Linear(hidden_size, hidden_size)
        self.ff2 = torch.nn.Linear(hidden_size, hidden_size)
        self.drop = torch.nn.Dropout(drop_rate)

    def forward(self, input_data):
        """H * T + X * ( 1 - T)

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """        

        hh = torch.relu(self.ff1(input_data))
        tt = torch.sigmoid(self.ff2(input_data))

        return self.drop(hh*tt+input_data*(1-tt))
