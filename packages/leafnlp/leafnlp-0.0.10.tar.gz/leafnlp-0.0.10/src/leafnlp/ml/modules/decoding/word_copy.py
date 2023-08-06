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


def word_copy(beam_seq,
              beam_attn,
              src_mask,
              src_arr,
              id2vocab,
              ext_id2oov,
              copy_words: bool = False,
              beam_size: int = 5,
              batch_size: int = 10,
              src_seq_lens: int = 100):
    """This is a meta-algorithm that can combine with 
    any seq2seq models to replace OOV words.
    Copy word from source to summary based on attention weights.

    Args:
        * ``beam_seq`` (_type_): _description_
        * ``beam_attn`` (_type_): _description_
        * ``src_mask`` (_type_): _description_
        * ``src_arr`` (_type_): _description_
        * ``id2vocab`` (_type_): _description_
        * ``ext_id2oov`` (_type_): _description_
        * ``copy_words`` (**bool**, optional): _description_. Defaults to False.
        * ``beam_size`` (**int**, optional): _description_. Defaults to 5.
        * ``batch_size`` (**int**, optional): _description_. Defaults to 10.
        * ``src_seq_lens`` (**int**, optional): _description_. Defaults to 100.

    Returns:
        _type_: _description_
    """

    out_arr = []
    if copy_words:
        src_mask = src_mask.repeat(1, beam_size).view(
            src_mask.size(0), beam_size, src_seq_lens).unsqueeze(0)
        beam_attn = beam_attn*src_mask
        beam_copy = beam_attn.topk(1, dim=3)[1].squeeze(-1)
        beam_copy = beam_copy[:, :, 0].transpose(0, 1)
        wdidx_copy = beam_copy.data.cpu().numpy()
        for b in range(batch_size):
            gen_text = beam_seq.data.cpu().numpy()[b, 0]
            gen_text = [id2vocab[wd] if wd in id2vocab else ext_id2oov[wd]
                        for wd in gen_text]
            gen_text = gen_text[1:]
            for j in range(len(gen_text)):
                if gen_text[j] == '<unk>':
                    gen_text[j] = src_arr[b][wdidx_copy[b, j]]
            out_arr.append(' '.join(gen_text))
    else:
        for b in range(batch_size):
            gen_text = beam_seq.data.cpu().numpy()[b, 0]
            gen_text = [id2vocab[wd] if wd in id2vocab else ext_id2oov[wd]
                        for wd in gen_text]
            gen_text = gen_text[1:]
            out_arr.append(' '.join(gen_text))

    return out_arr
