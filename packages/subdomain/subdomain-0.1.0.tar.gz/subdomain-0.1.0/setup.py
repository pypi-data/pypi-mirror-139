# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subdomain']

package_data = \
{'': ['*'], 'subdomain': ['dict/*']}

install_requires = \
['IPy>=1.01,<2.0',
 'aiodns>=3.0.0,<4.0.0',
 'autopep8>=1.6.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'subdomain',
    'version': '0.1.0',
    'description': '这是一个使用异步协程的子域名爆破工具。',
    'long_description': None,
    'author': 'zmf96',
    'author_email': 'zmf96@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
