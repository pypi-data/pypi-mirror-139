# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evalify', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16.0,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'scikit-learn>=1.0.0,<2.0.0']

extras_require = \
{'dev': ['tox>=3.24.5,<4.0.0',
         'virtualenv>=20.13.1,<21.0.0',
         'pip>=22.0.3,<23.0.0',
         'twine>=3.8.0,<4.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'livereload>=2.6.3,<3.0.0'],
 'test': ['black==22.1.0',
          'isort==5.10.1',
          'flake8==4.0.1',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'pyreadline>=2.1,<3.0']}

setup_kwargs = {
    'name': 'evalify',
    'version': '0.1.0',
    'description': 'Evaluate your face verification models literally in seconds.',
    'long_description': '# evalify\n\n<p align="center">\n\n<img src="https://user-images.githubusercontent.com/7144929/154332210-fa1fee34-faae-4567-858a-49fa53e99a2b.svg" width="292" height="120" alt="Logo"/>\n\n</p>\n\n<p align="center">\n\n<a href="https://github.com/ma7555/evalify/blob/main/LICENSE">\n    <img src="https://img.shields.io/github/license/ma7555/evalify"\n        alt = "License">\n</a>\n\n<a href="https://www.python.org/downloads/">\n    <img src="https://img.shields.io/badge/python-3.7 | 3.8 | 3.9 | 3.10-blue.svg"\n        alt = "Python 3.7 | 3.8 | 3.9">\n</a>\n\n<a href="https://pypi.python.org/pypi/evalify">\n    <img src="https://img.shields.io/pypi/v/evalify.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/ma7555/evalify/actions">\n    <img src="https://github.com/ma7555/evalify/actions/workflows/dev.yml/badge.svg?branch=main" alt="CI Status">\n</a>\n\n<a href="https://ma7555.github.io/evalify/">\n    <img src="https://img.shields.io/website/https/ma7555.github.io/evalify/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">\n</a>\n\n<a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">\n</a>\n\n<a href="https://codecov.io/gh/ma7555/evalify">\n  <img src="https://codecov.io/gh/ma7555/evalify/branch/main/graph/badge.svg" />\n</a>\n\n<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/ma7555/evalify/total">\n\n<!-- <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ma7555/evalify"> -->\n\n</p>\n\n\nEvaluate your face verification models literally in seconds.\n\n## Installation\n#### Stable release\n```bash\npip install evalify\n```\n#### Bleeding edge\n* From source\n    ```bash\n    pip install git+https://github.com/ma7555/evalify.git\n    ```\n* From TestPyPI\n    ```bash\n    pip install --index-url https://test.pypi.org/simple/evalify\n    ```\n\n## Usage\n\n```python\nimport numpy as np\nfrom evalify import Experiment\n\nrng = np.random.default_rng()\nnphotos = 500\nemb_size = 32\nnclasses = 10\nX = rng.random((self.nphotos, self.emb_size))\ny = rng.integers(self.nclasses, size=self.nphotos)\n\nexperiment = Experiment()\nexperiment.run(X, y)\nexperiment.get_roc_auc()\nprint(experiment.df.roc_auc)\n```\n\n## Documentation: \n* <https://ma7555.github.io/evalify/>\n\n\n## Features\n\n* Blazing fast implementation for metrics calculation through optimized einstein sum.\n* Many operations are dispatched to canonical BLAS, cuBLAS, or other specialized routines.\n* Smart sampling options using direct indexing from pre-calculated arrays.\n* Supports common evaluation metrics like cosine similarity, euclidean distance and l2 normalized euclidean distance.\n\n## Contribution\n* Contributions are welcomed, and they are greatly appreciated! Every little bit helps, and credit will always be given.\n* Please check [CONTRIBUTING.md](https://github.com/ma7555/evalify/blob/main/CONTRIBUTING.md) for guidelines.\n\n## Citation\n* If you use this software, please cite it using the metadata from [CITATION.cff](https://github.com/ma7555/evalify/blob/main/CITATION.cff)\n\n',
    'author': 'Mahmoud Bahaa',
    'author_email': 'mah.alaa@nu.edu.eg',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ma7555/evalify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
