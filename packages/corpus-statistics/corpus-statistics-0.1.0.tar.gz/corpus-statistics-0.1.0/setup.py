# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['corpus_statistics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'spacy>=3.2.2,<4.0.0',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'spacy_factories': ['simple_corpus_stats = '
                     'corpus_statistics.component_simple:create_simple_corpus_stats_component']}

setup_kwargs = {
    'name': 'corpus-statistics',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Corpus Statistics: A Very Basic (for now) spaCy Pipeline Component\n\nIf you want to know what tokens your pipeline has seen, this is the component for you.\n\n```bash\npip install git+https://github.com/pmbaumgartner/corpus_statistics\n```\n\n⚡️ **Example**\n\n```python\nfrom spacy.lang.en import English\n\n# Use some example data\nfrom datasets import load_dataset\ndataset = load_dataset("imdb")\ntexts = dataset["train"]["text"]\n\n# ✨ start the magic \nnlp = English()  # or spacy.load(\'a_model\')\nnlp.add_pipe("simple_corpus_stats")\n\nfor doc in nlp.pipe(texts):\n    # ➡️ do your pipeline stuff! ➡️\n    pass\n\ncorpus_stats = nlp.get_pipe("simple_corpus_stats")\n\n# check if a token has been processed through this pipeline\ntoken = "apple"\nif token in corpus_stats:\n    token_count = corpus_stats[token]\n    print(f"\'{token}\' mentioned {token_count} times")\n\n# \'apple\' mentioned 24 times\n```\n\nIt\'s got all your favorite [legomena](https://en.wikipedia.org/wiki/Hapax_legomenon) like `hapax` and `dis`.\n\n```python\nonly_seen_once = len(corpus_stats.hapax_legomena)\npercent_of_vocab = only_seen_once / corpus_stats.vocab_size\nprint(f"{percent_of_vocab*100:.1f}% tokens only occurred once.")\n# 47.6% tokens only occurred once.\n\nonly_seen_twice = len(corpus_stats.dis_legomena)\npercent_of_vocab_2x = only_seen_twice / corpus_stats.vocab_size\nprint(f"{percent_of_vocab_2x*100:.1f}% tokens occurred twice.")\n# 12.3% tokens occurred twice.\n```\n\nWe counted some things too:\n\n```python\n# corpus_stats.vocabulary is a collections.Counter 🔢\nprint(*corpus_stats.vocabulary.most_common(5), sep="\\n")\n# (\'the\', 289838)\n# (\',\', 275296)\n# (\'.\', 236702)\n# (\'and\', 156484)\n# (\'a\', 156282)\n\nmean_doc_length = sum(corpus_stats.doc_lengths) / corpus_stats.corpus_length\nprint(f"Mean doc length: {mean_doc_length:.1f}")\n# Mean doc length: 272.5\n```\n\n# Use in Model Training and Config Files\n\nThis can be quite helpful if you wanted to know what tokens were seen in your training data. You can include this component in your training config as follows.\n\n```\n...\n[nlp]\nlang = "en"\npipeline = ["simple_corpus_stats", ...]\n...\n\n[components]\n\n[components.simple_corpus_stats]\nfactory = "simple_corpus_stats"\nn_train = 1000  # This is important! See below\n```\n\n⚠️ 🔁 If you use this component in a training config, your pipeline will see the same docs multiple times, due to the number of training epochs and evaluation steps, so the vocab counter will be incorrect. To correct for this, you need to specify the number of examples in your training dataset as the `n_train` config parameter. \n\n```python\nimport spacy\n\nnlp = spacy.load("your_trained_model")\ncorpus_stats = nlp.get_pipe("simple_corpus_stats")\n\nassert min(corpus_stats.vocabulary.values()) == 1\n\n# value from config\nassert len(corpus_stats.doc_lengths) == 1000\n```\n\n\n',
    'author': 'Peter Baumgartner',
    'author_email': '5107405+pmbaumgartner@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
