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
    'version': '0.2.1',
    'description': '',
    'long_description': '# pych-client\n\n[![Coverage][coverage-badge]][coverage-url]\n[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]\n[![Tests Status][tests-workflow-badge]][tests-workflow-url]\n[![PyPI][pypi-badge]][pypi-url]\n\npych-client is a [ClickHouse][clickhouse] client for Python. It targets the HTTP interface and offers the following\nfeatures:\n- Sync (`ClickHouseClient`) and async (`AsyncClickHouseClient`) clients.\n- Streaming requests and responses.\n- Optionally load credentials from the environment variables, or from a configuration file.\n\n## Installation\n\n```bash\n# Default Python JSON parser:\npip install pych-client\n# Faster orjson parser:\npip install pych-client[orjson]\n```\n\n## Usage\n\n```python\nfrom pych_client import ClickHouseClient\n\nparams = {"table": "test_pych"}\nwith ClickHouseClient() as client:\n    client.text(\'\'\'\n        CREATE TABLE {table:Identifier} (a Int64, b Int64)\n        ENGINE MergeTree() ORDER BY (a, b)\n    \'\'\', params)\n    client.text("INSERT INTO {table:Identifier} VALUES", params, "(1, 2), (3, 4)")\n    client.text("INSERT INTO {table:Identifier} VALUES", params, [b"(5, 6)", b"(7, 8)"])\n    client.json("SELECT * FROM {table:Identifier} ORDER BY a", params)\n# [{\'a\': \'1\', \'b\': \'2\'}, {\'a\': \'3\', \'b\': \'4\'}, {\'a\': \'5\', \'b\': \'6\'}, {\'a\': \'7\', \'b\': \'8\'}]\n```\n\n### Command-line interface\n\n```bash\npipx install pych-client\npych-client --help\n```\n\n### Credential provider chain\n\nThe client looks for credentials in a way similar to the [AWS SDK][aws-sdk]:\n\n1. If one of `base_url`, `database`, `username` or `password` is specified, these values will be used.\n2. If none of the previous values are specified, and one of `PYCH_BASE_URL`, `PYCH_DATABASE`, `PYCH_USERNAME`\n   or `PYCH_PASSWORD` environment variables are present, these values will be used.\n3. If none of the previous values are specified, and the file `~/.config/pych-client/credentials.json` exists, the\n   fields `base_url`, `database` and `username` and `password` will be used.\n4. If none of the previous values are specified, the values `http://localhost:8213`, `default` and `default`\n   will be used.\n\n[aws-sdk]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html\n\n[clickhouse]: https://clickhouse.com\n\n[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/pych-client?logo=codecov&logoColor=white\n\n[coverage-url]: https://codecov.io/gh/dioptra-io/pych-client\n\n[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/PyPI?logo=github&label=pypi\n\n[pypi-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/pypi.yml\n\n[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/Tests?logo=github&label=tests\n\n[tests-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/tests.yml\n\n[pypi-badge]: https://img.shields.io/pypi/v/pych-client?logo=pypi&logoColor=white\n\n[pypi-url]: https://pypi.org/project/pych-client/\n',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
