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
import logging
import os

import requests
import torch
from leafnlp.ml.modules.encoder.encoder_rnn import EncoderRNN
from torch.autograd import Variable
from transformers import BertModel, BertTokenizer


class model_sequence_tagging(object):
    """Event Detection Model

    Args:
        * ``model_param`` (**str**, optional): Defaults to None.

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
                 model_param=None,
                 train_model_dir="model",
                 base_model_dir="",
                 task="production",
                 device="cpu"):
        self.task = task
        self.train_model_dir = train_model_dir
        if not base_model_dir:
            self.base_model_dir = train_model_dir
        else:
            self.base_model_dir = base_model_dir
        self.device = device
        self.model_param = model_param

        self.pretrained_models = {}
        self.train_models = {}
        self.base_models = {}
        self.batch_data = {}

        if self.task in ["production"]:
            logging.disable(logging.INFO)
            logging.disable(logging.WARNING)

        self.tokenizer = BertTokenizer.from_pretrained(
            "bert-base-cased")

        if self.task in ["production"]:
            self._build_vocabulary()
            if not self.model_param == "customized":
                PATH_HOME = os.path.expanduser("~")
                PATH_LEAFNLP = os.path.join(PATH_HOME, ".leafnlp_data")
                if not os.path.exists(PATH_LEAFNLP):
                    os.mkdir(PATH_LEAFNLP)
                PATH_LEAFNLP_MODELS_NER_MODEL = os.path.join(
                    PATH_LEAFNLP, self.model_param)
                if not os.path.exists(PATH_LEAFNLP_MODELS_NER_MODEL):
                    os.mkdir(PATH_LEAFNLP_MODELS_NER_MODEL)
                self.base_model_dir = PATH_LEAFNLP_MODELS_NER_MODEL
                self.train_model_dir = PATH_LEAFNLP_MODELS_NER_MODEL
                url_head = "https://leafnlp.s3.amazonaws.com"
                # Download label mapping
                model_file = "{}/label_mapping.json".format(
                    PATH_LEAFNLP_MODELS_NER_MODEL)
                if not os.path.exists(model_file):
                    url = "{}/.leafnlp_data/{}/label_mapping.json".format(
                        url_head, self.model_param)
                    fout = open(model_file, "wb")
                    res = requests.get(url, stream=True)
                    for chunk in res:
                        fout.write(chunk)
                    fout.close()
                # Load label_mapping
                fl1_ = "{}/label_mapping.json".format(self.train_model_dir)
                with open(fl1_, "r") as fp:
                    label_mapping = json.load(fp)
                self.label2id = {key: label_mapping[key]
                                 for key in label_mapping}
                self.id2label = {label_mapping[key]: key for key in label_mapping}
                self.n_labels = len(self.label2id)
                # build model
                self._build_models()
                # download model param
                for model_name in list(self.base_models) + list(self.train_models):
                    model_file = "{}/{}.model".format(
                        PATH_LEAFNLP_MODELS_NER_MODEL, model_name)
                    if not os.path.exists(model_file):
                        logging.info("Download {}".format(model_file))
                        fout = open(model_file, "wb")
                        url = "{}/.leafnlp_data/{}/{}.model".format(
                            url_head, self.model_param, model_name)
                        res = requests.get(url, stream=True)
                        for chunk in res:
                            fout.write(chunk)
                        fout.close()
            else:
                self._build_models()
            # load model param
            for mode_name in self.pretrained_models:
                self.pretrained_models[mode_name].eval()
            for model_name in self.base_models:
                self.base_models[model_name].eval()
                model_file = "{}/{}.model".format(
                    self.base_model_dir, model_name)
                self.base_models[model_name].load_state_dict(torch.load(
                    model_file, map_location=lambda storage, loc: storage))
            for model_name in self.train_models:
                self.train_models[model_name].eval()
                model_file = "{}/{}.model".format(
                    self.train_model_dir, model_name)
                self.train_models[model_name].load_state_dict(torch.load(
                    model_file, map_location=lambda storage, loc: storage))

    def _build_vocabulary(self):
        """Build Vocabulary
        """
        vocab2id = self.tokenizer.get_vocab()
        id2vocab = {vocab2id[wd]: wd for wd in vocab2id}
        vocab_size = len(id2vocab)
        self.batch_data["vocab2id"] = id2vocab
        self.batch_data["id2vocab"] = vocab2id
        logging.info("The vocabulary size: {}".format(vocab_size))

    def _build_models(self):
        """Build all models.
        """
        hidden_size = 768
        self.pretrained_models["bert"] = BertModel.from_pretrained(
            "bert-base-cased",
            output_hidden_states=True,
            output_attentions=True).to(self.device)
        self.TOK_START = 101
        self.TOK_END = 102
        self.TOK_PAD = 0

        self.train_models["encoder"] = EncoderRNN(
            emb_dim=hidden_size,
            hidden_size=hidden_size,
            nLayers=2,
            rnn_network="lstm",
            device=self.device).to(self.device)

        self.train_models["classifier"] = torch.nn.Linear(
            hidden_size*2, self.n_labels).to(self.device)

    def _build_pipe(self):
        """Shared pipe
        """
        with torch.no_grad():
            input_emb = self.pretrained_models["bert"](
                self.batch_data["input_ids"],
                self.batch_data["pad_mask"])[0]

        input_enc, _ = self.train_models["encoder"](input_emb)

        logits = self.train_models["classifier"](torch.relu(input_enc))

        return logits

    def _build_batch(self, batch_data):
        """Build Batch
        """
        token_arr = []
        input_data_raw = []
        maxlen_text = 0
        for itm in batch_data:
            if self.task in ["production"]:
                toks = self.tokenizer.encode(itm["text"])[1:-1][:300]
                itm["tokens"] = self.tokenizer.convert_ids_to_tokens(toks)
            else:
                itm = json.loads(itm)
                assert "tokens" in itm
                if len(itm["tokens"]) > 300:
                    continue
                toks = self.tokenizer.convert_tokens_to_ids(itm["tokens"])
            input_data_raw.append(itm)
            toks = [self.TOK_START] + toks + [self.TOK_END]
            token_arr.append(toks)
            if maxlen_text < len(toks):
                maxlen_text = len(toks)

        self.batch_data["maxlen_text"] = maxlen_text

        token_arr = [itm[:maxlen_text] for itm in token_arr]
        token_arr = [itm + [self.TOK_PAD for _ in range(maxlen_text-len(itm))]
                     for itm in token_arr]
        token_var = Variable(torch.LongTensor(token_arr))

        pad_mask = Variable(torch.FloatTensor(token_arr))
        pad_mask[pad_mask != float(self.TOK_PAD)] = -1.0
        pad_mask[pad_mask == float(self.TOK_PAD)] = 0.0
        pad_mask = -pad_mask

        self.batch_data["input_ids"] = token_var.to(self.device)
        self.batch_data["pad_mask"] = pad_mask.to(self.device)
        self.batch_data["input_data_raw"] = input_data_raw
