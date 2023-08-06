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

import json
from typing import Dict, List

import torch
from leafnlp.ml.sequence_tagging.bert import model_sequence_tagging

from .utils import clean_result


class modelNER(model_sequence_tagging):
    """Named Entity Recogonition Model

    Args:
        * ``model_param`` (**str**, optional): Defaults to "model_ner_bert_v1".

        Option for model parameters. If "customized", please specify `train_model_dir` and `base_model_dir`.

        * ``train_model_dir`` (**str**, optional): Defaults to "model".
        * ``base_model_dir`` (**str**, optional): Defaults to "".

        If not specified, `base_model_dir` will be the same as `train_model_dir`

        * ``task`` (**str**, optional): Defaults to "production".

        Options for Task: `train`, `validate`, `test`, `production`.

        * ``device`` (**str**, optional): Defaults to "cpu".

        Device: e.g. `cpu` and `cuda:0`.
    """

    def __init__(self,
                 model_param="model_ner_bert_conll2003",
                 train_model_dir="model",
                 base_model_dir="",
                 task="production",
                 device="cpu"):
        super().__init__(model_param=model_param, 
                         train_model_dir=train_model_dir, 
                         base_model_dir=base_model_dir, 
                         task=task, 
                         device=device)

    def _get_raw_results(self, 
                         batch_text: List, 
                         top_n: int = 5):
        """Get raw results.

        Args:
            * ``batch_text`` (**list**): All input texts.
        """
        assert isinstance(batch_text, List)
        batch_data = []
        for itm in batch_text:
            if not isinstance(itm, Dict):
                try:
                    itm = json.loads(itm)
                except:
                    itm = {"text": itm}
            batch_data.append(itm)
        self._build_batch(batch_data)
        with torch.no_grad():
            logits = self._build_pipe()
            logits = torch.softmax(logits, dim=2)

        prob, labels = logits.topk(self.n_labels, dim=2)
        prob = prob.squeeze(2)
        prob = prob.data.cpu().numpy().tolist()
        labels = labels.squeeze(2)
        labels = labels.data.cpu().numpy().tolist()

        for k, itm in enumerate(self.batch_data["input_data_raw"]):

            lname = [self.id2label[lb[0]] for lb in labels[k]]
            itm["labels"] = lname[1:][:len(itm["tokens"])]

            lcand = []
            for arr in labels[k]:
                out = []
                for lb in arr[:top_n]:
                    out.append(self.id2label[lb])
                lcand.append(out)
            lcand = lcand[1:][:len(itm["tokens"])]
            itm["cand_labels"] = lcand
            itm["cand_prob"] = [arr[:top_n] for arr in prob[k]][1:][:len(itm["tokens"])]

            yield clean_result(itm)
            
    def annotate_raw_dump(self, 
                          input_text: List, 
                          top_n: int = 5, 
                          batch_size: int = 10):
        """Get raw annotation results.

        Args:
            * ``input_text`` (**List**): input texts.
            * ``top_n`` (**int**, optional): Top n candidate labels. Defaults to 10.
            * ``batch_size`` (**int**, optional): batch size. Defaults to 10.

        Returns:
            * ``Dict``: Output
        """        
        
        if not isinstance(input_text, List):
            input_text = [input_text]
        batch_size = min(batch_size, len(input_text))

        k = 0
        output = []
        while k * batch_size < len(input_text):
            batch_text = input_text[k*batch_size:(k+1)*batch_size]
            results = self._get_raw_results(batch_text, top_n)

            output = [itm for itm in results]
            k += 1

        return output
        

    def annotate(self, 
                 input_text: List, 
                 batch_size: int = 10):
        """Annotate texts.

        Args:
            * ``input_text`` (**List**): input texts
            * ``batch_size`` (**int**): batch_size

        Examples::

            >>> from leafnlp.nlp.named_entity_recogonition.bert import modelNER

            >>> model = modelNER(device="cuda:0")

            >>> input_text = [{"text": "The storm hits New York."}]
            >>> input_text = ["The storm hits New York."]
            >>> output = model.annotate(input_text)
            >>> print(output)
        """
        if not isinstance(input_text, List):
            input_text = [input_text]
        batch_size = min(batch_size, len(input_text))

        k = 0
        output = []
        while k * batch_size < len(input_text):
            batch_text = input_text[k*batch_size:(k+1)*batch_size]
            results = self._get_raw_results(batch_text)

            for itm in results:
                out = {
                    "text": itm["text"],
                    "named_entities": itm["named_entities"]}
                output.append(out)
            k += 1

        return output
