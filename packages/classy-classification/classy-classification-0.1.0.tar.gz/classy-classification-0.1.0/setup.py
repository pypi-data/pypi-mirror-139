# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_classification',
 'classy_classification.classifiers',
 'classy_classification.examples']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=1.0.2,<2.0.0',
 'sentence-transformers>=2.2.0,<3.0.0',
 'spacy[transformers]>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'classy-classification',
    'version': '0.1.0',
    'description': 'This repository contains an easy and intuitive approach to few-shot text classification using sentence-transformers and spacy embeddings.',
    'long_description': '# Classy few shot classification\nThis repository contains an easy and intuitive approach to few-shot text classification. \n\n# Why?\n[Huggingface](https://huggingface.co/) does offer some nice models for few/zero-shot classification, but these are not tailored to multi-lingual approaches. Rasa NLU has [a nice approach](https://rasa.com/blog/rasa-nlu-in-depth-part-1-intent-classification/) for this, but its to embedded in their codebase for easy usage outside of Rasa/chatbots. Additionally, it made sense to integrate [sentence-transformers](https://github.com/UKPLab/sentence-transformers), instead of default [word embeddings](https://arxiv.org/abs/1301.3781). Finally, I decided to integrate with Spacy, since training a custom [Spacy TextCategorizer](https://spacy.io/api/textcategorizer) seems like a lot of hassle if you want something quick. \n\n# Install\n``` pip install classy-classification```\n# Quickstart\nTake a look at the examples directory. \n## Some quick and dirty training data.\n``` \ntraining_data = {\n    "politics": [\n        "Putin orders troops into pro-Russian regions of eastern Ukraine.",\n        "The president decided not to go through with his speech.",\n        "There is much uncertainty surrounding the coming elections.",\n        "Democrats are engaged in a ‘new politics of evasion’"\n    ],\n    "sports": [\n        "The soccer team lost.",\n        "The team won by two against zero.",\n        "I love all sport.",\n        "The olympics were amazing.",\n        "Yesterday, the tennis players wrapped up wimbledon."\n    ],\n    "weather": [\n        "It is going to be sunny outside.",\n        "Heavy rainfall and wind during the afternoon.",\n        "Clear skies in the morning, but mist in the evenening.",\n        "It is cold during the winter.",\n        "There is going to be a storm with heavy rainfall."\n    ]\n}\n\nvalidation_data = [\n    "I am surely talking about politics.",\n    "Sports is all you need.",\n    "Weather is amazing."\n]\n```\n\n\n## using an individual sentence-transformer\n```\nfrom classy_classification import classyClassifier\n\nclassifier = classyClassifier(data=training_data)\nclassifier(validation_data[0])\nclassifier.pipe(validation_data)\n\n# overwrite training data\nclassifier.set_training_data(data=new_training_data)\n\n# overwrite [embedding model](https://www.sbert.net/docs/pretrained_models.html)\nclassifier.set_embedding_model(model="paraphrase-MiniLM-L3-v2")\n\n# overwrite SVC config\nclassifier.set_svc(\n    config={                              \n        "C": [1, 2, 5, 10, 20, 100],\n        "kernels": ["linear"],                              \n        "max_cross_validation_folds": 5\n    }\n)\n```\n\n## external sentence-transformer within spacy pipeline\n```\nimport spacy\n\nimport classy_classification\n\nnlp = spacy.blank("en")\nnlp.add_pipe("text_categorizer", config={"data": training_data}) # provide similar config as above\nnlp(validation_data[0])._.cats\nnlp.pipe(validation_data)\n```\n## internal spacy word2vec embeddings\n```\nimport spacy\n\nimport classy_classification\n\nnlp = spacy.load("en_core_web_md") \nnlp.add_pipe("text_categorizer", config={"data": training_data, "model": "spacy"}) #use internal embeddings from spacy model\nnlp(validation_data[0])._.cats\nnlp.pipe(validation_data)\n```\n\n# Todo\n[ ] look into a way to integrate spacy trf models.\n\n\n# Inspiration Drawn From\n- [Scikit-learn](https://github.com/scikit-learn/scikit-learn)\n- [Rasa NLU](https://github.com/RasaHQ/rasa) \n- [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)\n- [Spacy](https://github.com/explosion/spaCy)\n',
    'author': 'David Berenstein',
    'author_email': 'david.berenstein@pandoraintelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidberenstein1957/classy-classification',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
