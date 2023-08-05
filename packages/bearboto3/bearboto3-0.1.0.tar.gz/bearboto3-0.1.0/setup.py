# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bearboto3']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.9.0,<0.10.0']

extras_require = \
{'dynamodb': ['dynamodb-stubs[dynamodb]>=1.20.26,<2.0.0'],
 'ec2': ['ec2-stubs[ec2]>=1.20.26,<2.0.0'],
 'iam': ['iam-stubs[iam]>=1.20.26,<2.0.0'],
 'lambda': ['lambda-stubs[lambda]>=1.20.26,<2.0.0'],
 's3': ['s3-stubs[s3]>=1.20.26,<2.0.0'],
 'sns': ['sns-stubs[sns]>=1.20.26,<2.0.0'],
 'sqs': ['sqs-stubs[sqs]>=1.20.26,<2.0.0']}

setup_kwargs = {
    'name': 'bearboto3',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Paul',
    'author_email': 'dev@studiop.page',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
