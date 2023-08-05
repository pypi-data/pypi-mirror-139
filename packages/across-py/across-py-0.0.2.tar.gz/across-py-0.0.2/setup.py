# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['across']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'across-py',
    'version': '0.0.2',
    'description': 'across sdk in python',
    'long_description': '# Across\n\nAcross is the fastest, cheapest and most secure cross-chain bridge. It is a system that uses UMA contracts to quickly move tokens across chains. This contains various utilities to support applications on across.\n\n## How to use\n\nUse across official API to get suggested fees.\n```py\n>>> import across\n>>> a = across.AcrossAPI()\n>>> a.suggested_fees("0x7f5c764cbc14f9669b88837ca1490cca17c31607", 10, 1000000000)\n{\'slowFeePct\': \'43038790000000000\', \'instantFeePct\': \'5197246000000000\'}\n```\n\n## How to build and test\n\nInstall poetry and install the dependencies:\n\n```shell\npip3 install poetry\n\npoetry install\n\n# test\npython -m unittest\n\n# local install and test\npip3 install twine\npython3 -m twine upload --repository testpypi dist/*\npip3 install --index-url https://test.pypi.org/simple/ --no-deps across\n```\n',
    'author': 'qiwihui',
    'author_email': 'qwh005007@gmail.com',
    'maintainer': 'qiwihui',
    'maintainer_email': 'qwh005007@gmail.com',
    'url': 'https://github.com/qiwihui/across-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
