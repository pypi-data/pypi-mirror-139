# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywisetransfer']

package_data = \
{'': ['*']}

install_requires = \
['apiron>=6.1.0,<7.0.0', 'cryptography>=36.0.1,<37.0.0', 'munch>=2.5.0,<3.0.0']

extras_require = \
{'dev': ['black>=22.1.0,<23.0.0',
         'pytest>=7.0.1,<8.0.0',
         'responses>=0.18.0,<0.19.0']}

setup_kwargs = {
    'name': 'pywisetransfer',
    'version': '0.2.0',
    'description': 'Python library for the TransferWise API',
    'long_description': '# pywisetransfer\n\nAn unofficial, experimental Python client library for the [TransferWise API](https://api-docs.transferwise.com).\n\n:warning: The classes, functions and interfaces that this library provides are very much in-development and prone to change.\n\n## Installation\n\n```bash\n# Within your project directory\npoetry add pywisetransfer\n```\n\n## Usage\n\n### API Requests\n\n```python\nimport pywisetransfer\n\nclient = pywisetransfer.Client(api_key="your-api-key-here")\n\nfor profile in client.profiles.list():\n    accounts = client.borderless_accounts.list(profile_id=profile.id)\n    for account in accounts:\n        currencies = [balance.currency for balance in account.balances]\n        print(f"AccountID={account.id}, Currencies={currencies}")\n```\n\n### Webhook signature verification\n\n```python\nimport pywisetransfer\nfrom pywisetransfer.webhooks import verify_signature\n\npayload = b"webhook-request-body-here"\nsignature = "webhook-signature-data-here"\n\nvalid = verify_signature(payload, signature)\nprint(f"Valid webhook signature: {valid}")\n\n```\n\n## Run tests\n\n```bash\n# Within the pywisetransfer working directory\npip install .[dev]\npytest\n```\n',
    'author': 'James Addison',
    'author_email': 'jay@jp-hosting.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/jayaddison/pywisetransfer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
