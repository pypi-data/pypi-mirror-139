# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyeuropeana', 'pyeuropeana.apis', 'pyeuropeana.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4,<0.5',
 'pandas>=1.3,<2.0',
 'pillow>=9.0.0,<10.0.0',
 'requests>=2.27,<3.0']

setup_kwargs = {
    'name': 'pyeuropeana',
    'version': '0.1.2',
    'description': 'A Python wrapper around Europeana APIs',
    'long_description': '# Python interface for Europeana\'s APIs\n\nThis package is a Python wrapper for Europeana\'s [Search](https://pro.europeana.eu/page/search) and [Record](https://pro.europeana.eu/page/record) APIs.\n\n## Installation\n\nAs this package is not published on PyPI currently, the only way to install it is through its Git repository host using pip:\n\n`pip install https://github.com/europeana/rd-europeana-python-api/archive/stable.zip`\n\nFrom source\n\n`git clone https://github.com/europeana/rd-europeana-python-api.git`\n\n`cd rd-europeana-python-api`\n\n`pip install -e .`\n\n## Authentication\n\nGet your API key [here](https://pro.europeana.eu/pages/get-api)\n\nSet `EUROPEANA_API_KEY` as an environment variable running `export EUROPEANA_API_KEY=yourapikey` in the terminal.\n\nIf running in Google Colab use `os.environ[\'EUROPEANA_API_KEY\'] = \'yourapikey\'`\n\n## Usage\n\n\n```python\nfrom pyeuropeana.apis import SearchWrapper\nfrom pyeuropeana.utils.edm_utils import res2df\n\nresult = SearchWrapper(\n  query = \'*\',\n  qf = \'(skos_concept:"http://data.europeana.eu/concept/base/48" AND TYPE:IMAGE)\',\n  reusability = \'open AND permission\',\n  media = True,\n  thumbnail = True,\n  landingpage = True,\n  colourpalette = \'#0000FF\',\n  theme = \'photography\',\n  sort = \'europeana_id\',\n  profile = \'rich\',\n  rows = 1000,\n) # this gives you full response metadata along with cultural heritage object metadata\n\n# use this utility function to transform a subset of the cultural heritage object metadata\n# into a readable Pandas DataFrame\ndataframe = res2df(result, full=False)\n```\n\n[Colab tutorial](https://colab.research.google.com/drive/1VZJn9JKqziSF2jVQz1HRsvgbUZ0FM7qD?usp=sharing)\n',
    'author': 'José Eduardo Cejudo Grano de Oro',
    'author_email': 'joseed.cejudo@europeana.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/europeana/rd-europeana-python-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
