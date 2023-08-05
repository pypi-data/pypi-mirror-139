# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pych_client']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

extras_require = \
{'orjson': ['orjson>=3.6.6,<4.0.0']}

entry_points = \
{'console_scripts': ['pych-client = pych_client.cli:main']}

setup_kwargs = {
    'name': 'pych-client',
    'version': '0.1.5',
    'description': '',
    'long_description': '# pych-client\n\n[![Coverage][coverage-badge]][coverage-url]\n[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]\n[![Tests Status][tests-workflow-badge]][tests-workflow-url]\n[![PyPI][pypi-badge]][pypi-url]\n\n## Installation\n\n```bash\n# Default Python JSON parser:\npip install pych-client\n# Faster orjson parser:\npip install pych-client[orjson]\n```\n\n## Usage\n\n```python\nfrom pych_client import ClickHouseClient\nparams = {"table": "test_pych"}\nwith ClickHouseClient() as client:\n    client.text(\'\'\'\n        CREATE TABLE {table:Identifier} (a Int64, b Int64)\n        ENGINE MergeTree() ORDER BY (a, b)\n    \'\'\', params)\n    client.text("INSERT INTO {table:Identifier} VALUES", params, "(1, 2), (3, 4)")\n    client.text("INSERT INTO {table:Identifier} VALUES", params, [b"(5, 6)", b"(7, 8)"])\n    client.json("SELECT * FROM {table:Identifier} ORDER BY a", params)\n# [{\'a\': \'1\', \'b\': \'2\'}, {\'a\': \'3\', \'b\': \'4\'}, {\'a\': \'5\', \'b\': \'6\'}, {\'a\': \'7\', \'b\': \'8\'}]\n```\n\n## Command-line interface\n\n```bash\npipx install pych-client\npych-client --help\n```\n\n[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/pych-client?logo=codecov&logoColor=white\n\n[coverage-url]: https://codecov.io/gh/dioptra-io/pych-client\n\n[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/PyPI?logo=github&label=pypi\n\n[pypi-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/pypi.yml\n\n[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/Tests?logo=github&label=tests\n\n[tests-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/tests.yml\n\n[pypi-badge]: https://img.shields.io/pypi/v/pych-client?logo=pypi&logoColor=white\n\n[pypi-url]: https://pypi.org/project/pych-client/\n',
    'author': 'Maxime Mouchet',
    'author_email': 'maxime.mouchet@lip6.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dioptra-io/pych-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
