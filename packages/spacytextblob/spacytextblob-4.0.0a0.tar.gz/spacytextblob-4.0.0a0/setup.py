# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacytextblob']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.0,<4.0', 'textblob>=0.15.3,<0.16.0']

setup_kwargs = {
    'name': 'spacytextblob',
    'version': '4.0.0a0',
    'description': 'A TextBlob sentiment analysis pipeline compponent for spaCy',
    'long_description': '# spacytextblob\n\n[![PyPI version](https://badge.fury.io/py/spacytextblob.svg)](https://badge.fury.io/py/spacytextblob)\n[![pytest](https://github.com/SamEdwardes/spacytextblob/actions/workflows/pytest.yml/badge.svg)](https://github.com/SamEdwardes/spacytextblob/actions/workflows/pytest.yml)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/spacytextblob?label=PyPi%20Downloads)\n[![Netlify Status](https://api.netlify.com/api/v1/badges/e2f2caac-7239-45a2-b145-a00205c3befb/deploy-status)](https://app.netlify.com/sites/spacytextblob/deploys)\n\nA TextBlob sentiment analysis pipeline component for spaCy. \n\n- [Docs](https://spacytextblob.netlify.app/)\n- [GitHub](https://github.com/SamEdwardes/spacytextblob)\n- [PyPi](https://pypi.org/project/spacytextblob/)\n\n## Table of Contents\n\n- [Install](#install)\n- [Quick Start](#quick-start)\n- [Quick Reference](#quick-reference)\n- [Reference and Attribution](#reference-and-attribution)\n\n## Install\n\nInstall *spacytextblob* from PyPi.\n\n```bash\npip install spacytextblob\n```\n\nTextBlob requires additional data to be downloaded before getting started.\n\n```bash\npython -m textblob.download_corpora\n```\n\nspaCy also requires that you download a model to get started.\n\n```bash\npython -m spacy download en_core_web_sm\n```\n\n## Quick Start\n\n*spacytextblob* allows you to access all of the attributes created of the `textblob.TextBlob` class but within the spaCy framework. The code below will demonstrate how to use *spacytextblob* on a simple string.\n\n```python\nimport spacy\nfrom spacytextblob.spacytextblob import SpacyTextBlob\n\nnlp = spacy.load(\'en_core_web_sm\')\ntext = "I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy."\nnlp.add_pipe("spacytextblob")\ndoc = nlp(text)\n\nprint(doc._.blob.polarity)\n# -0.125\n\nprint(doc._.blob.subjectivity)\n# 0.9\n\nprint(doc._.blob.sentiment_assessments.assessments)\n# [([\'really\', \'horrible\'], -1.0, 1.0, None), ([\'worst\', \'!\'], -1.0, 1.0, None), ([\'really\', \'good\'], 0.7, 0.6000000000000001, None), ([\'happy\'], 0.8, 1.0, None)]\n```\n\nIn comparison, here is how the same code would look using `TextBlob`:\n\n```python\nfrom textblob import TextBlob\n\ntext = "I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy."\nblob = TextBlob(text)\n\nprint(blob.sentiment_assessments.polarity)\n# -0.125\n\nprint(blob.sentiment_assessments.subjectivity)\n# 0.9\n\nprint(blob.sentiment_assessments.assessments)\n# [([\'really\', \'horrible\'], -1.0, 1.0, None), ([\'worst\', \'!\'], -1.0, 1.0, None), ([\'really\', \'good\'], 0.7, 0.6000000000000001, None), ([\'happy\'], 0.8, 1.0, None)]\n```\n\n## Quick Reference\n\n*spacytextblob* performs sentiment analysis using the [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html) library. Adding *spacytextblob* to a spaCy nlp pipeline creates a new extension attribute for the `Doc`, `Span`, and `Token` classes from spaCy.\n\n- `Doc._.blob`\n- `Span._.blob`\n- `Token._.blob`\n\nThe `._.blob` attribute contains all of the methods and attributes that belong to the `textblob.TextBlob` class Some of the common methods and attributes include: \n\n- **`._.blob.polarity`**: a float within the range [-1.0, 1.0].\n- **`._.blob.subjectivity`**: a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective. \n- **`._.blob.sentiment_assessments.assessments`**: a list of polarity and subjectivity scores for the assessed tokens.\n\nSee the [textblob docs](https://textblob.readthedocs.io/en/dev/api_reference.html#textblob.blob.TextBlob) for the complete listing of all attributes and methods that are available in `._.blob`.\n\n## Reference and Attribution\n\n- TextBlob\n    - [https://github.com/sloria/TextBlob](https://github.com/sloria/TextBlob)\n    - [https://textblob.readthedocs.io/en/latest/](https://textblob.readthedocs.io/en/latest/)\n- negspaCy (for inspiration in writing pipeline and organizing repo)\n    - [https://github.com/jenojp/negspacy](https://github.com/jenojp/negspacy)\n- spaCy custom components\n    - [https://spacy.io/usage/processing-pipelines#custom-components](https://spacy.io/usage/processing-pipelines#custom-components)\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/spaCyTextBlob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
