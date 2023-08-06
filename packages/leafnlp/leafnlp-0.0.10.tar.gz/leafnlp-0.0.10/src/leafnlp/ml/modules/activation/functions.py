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

import math

import torch
import torch.nn.functional as F


def gelu(input_):
    """GELU activation function.
    """
    return input_ * 0.5 * (1.0 + torch.erf(input_ / math.sqrt(2.0)))


def maxout(input_, pool_size):
    """maxout activation
    """
    input_size = list(input_.size())
    assert input_.size(-1) % pool_size == 0

    out_size = input_.size(-1) // pool_size
    input_size[-1] = out_size
    input_size.append(pool_size)

    return input_.view(*input_size).max(-1)


def sample_gumbel(shape, eps=1e-20):
    U = torch.rand(shape).cuda()
    return -torch.log(-torch.log(U + eps) + eps)


def gumbel_softmax_sample(logits, temperature):
    y = logits + sample_gumbel(logits.size())
    return F.softmax(y / temperature, dim=-1)


def gumbel_softmax(logits, temperature):
    """strait-through gumbel-softmax estimator
    Implementation borrowed from 
    https://gist.github.com/yzh119/fd2146d2aeb329d067568a493b20172f

    Args:
        * ``logits`` (_type_): _description_
        * ``temperature`` (_type_): _description_

    Returns:
        _type_: _description_
    """    
    
    y = gumbel_softmax_sample(logits, temperature)
    shape = y.size()
    _, ind = y.max(dim=-1)
    y_hard = torch.zeros_like(y).view(-1, shape[-1])
    y_hard.scatter_(1, ind.view(-1, 1), 1)
    y_hard = y_hard.view(*shape)
    return (y_hard - y).detach() + y
