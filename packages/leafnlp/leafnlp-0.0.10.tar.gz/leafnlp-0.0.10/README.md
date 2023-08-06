# LeafNLP - A package for domain specific natural language processing

This repository contains codes for LeafNLP.

## Installation
Use ``pip`` to install LeafNLP. Run:

```
pip install leafnlp
```

## Usage

```

from leafnlp.nlp.named_entity_recogonition.bert import modelNER
from pprint import pprint

model = modelNER()
input_text = [{"text": "The storm hits New York."}]
input_text = ["The storm arrived at New York."]

results = model.annotate(input_text)
results = model.annotate_raw_dump(input_text, top_n=10)

```

## Available Models

Task|Model|model_param|Note|
|-|-|-|-|
|NER|BERT|model_ner_bert_conll2003||
|ED|BERT|model_ed_bert_maven2020||

- ``NER``: Named Entity Recogonition.
- ``ED``: Event Detection.

## Acknowledgements

``LeafNLP`` is maintained by the LeafNLP Team.