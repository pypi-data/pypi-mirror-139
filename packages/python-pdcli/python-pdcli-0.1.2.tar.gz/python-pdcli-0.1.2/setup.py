# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pdcli', 'pdcli.api', 'pdcli.command']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0', 'pdpyras>=4.4.0']

entry_points = \
{'console_scripts': ['pd = pdcli.cli:pd']}

setup_kwargs = {
    'name': 'python-pdcli',
    'version': '0.1.2',
    'description': 'PD cli',
    'long_description': '# PD cli\n\n\n## Test\n```\nexport PD_ACCOUNT_TOKEN=xyz\n\npd ls \\\n  --statuses=acknowledged,triggered --since=$(date -v -1d +%F) --column \\\n  | column -t -s$\'\\t\'\n```\n\nDefault output is json string. In order to extract field:\n```shell\n# to extract "id" from user record\npd user --user-id=me | jq -r .id\n```\n\n\n## Reference\n* https://pypi.org/project/pdpyras/\n* https://developer.pagerduty.com/api-reference/\n',
    'author': 'King-On Yeung',
    'author_email': 'koyeung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/koyeung/python-pdcli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
