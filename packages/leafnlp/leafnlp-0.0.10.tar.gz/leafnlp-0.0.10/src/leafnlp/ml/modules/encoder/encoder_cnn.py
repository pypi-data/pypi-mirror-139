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

import re

import torch


class EncoderCNN(torch.nn.Module):
    """_summary_

    Args:
        * ``input_size`` (**int**): _description_
        * ``kernel_size`` (**str**): 3,4,5
        * ``kernel_nums`` (**str**): 100,100,100
        * ``device`` (_type_, optional): Device. Defaults to torch.device("cpu").
    """ 

    def __init__(self, 
                 input_size: int,
                 kernel_size: str,  
                 kernel_nums: str,
                 device=torch.device("cpu")):       
        super().__init__()

        kSize = re.split(',', kernel_size)
        kSize = [int(itm) for itm in kSize]
        kNums = re.split(',', kernel_nums)
        kNums = [int(itm) for itm in kNums]
        assert len(kSize) == len(kNums)

        self.convs1 = torch.nn.ModuleList([
            torch.nn.Conv2d(1, kNums[k], (kSize[k], input_size))
            for k in range(len(kNums))]).to(device)

    def forward(self, input_data):
        """_summary_

        Args:
            * ``input_data`` (_type_): _description_

        Returns:
            _type_: _description_
        """        

        input_data = input_data.unsqueeze(1)
        h0 = [torch.relu(conv(input_data)).squeeze(3) for conv in self.convs1]
        h0 = [torch.max_pool1d(k, k.size(2)).squeeze(2) for k in h0]
        h0 = torch.cat(h0, 1)

        return h0
