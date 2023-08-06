# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bearboto3']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.9.0,<0.10.0']

extras_require = \
{'dynamodb': ['mypy-boto3-dynamodb>=1.21.4,<2.0.0'],
 'ec2': ['mypy-boto3-ec2>=1.21.1,<2.0.0'],
 'iam': ['mypy-boto3-iam>=1.21.2,<2.0.0'],
 'lambda': ['mypy-boto3-lambda>=1.21.0,<2.0.0'],
 's3': ['mypy-boto3-s3>=1.21.0,<2.0.0'],
 'sns': ['mypy-boto3-sns>=1.21.0,<2.0.0'],
 'sqs': ['mypy-boto3-sqs>=1.21.0,<2.0.0']}

setup_kwargs = {
    'name': 'bearboto3',
    'version': '0.1.1',
    'description': 'Facilitates using beartype runtime type-checking with the AWS SDK',
    'long_description': "# bearboto3\n\nThis project provides support for using the [boto3](https://github.com/boto/boto3/) library (AWS Python SDK) and associated stub libraries such as [boto3-stubs](https://pypi.org/project/boto3-stubs/) together with [beartype](https://github.com/beartype/beartype/) for runtime type-checking.\n\nSince boto3 uses a data-driven factory model to create class types at runtime, you cannot annotate them without support of stub libraries such as `boto3-stubs`. However, if you are using a runtime type-checker such as `beartype`, type validation will fail since the types technically do not match (even though they represent the same object schema).\n\n_Behold..._\n\nthis project makes use of the [`typing.TYPE_CHECKING`](https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING) constant found in the python `typing` module to conditionally load either static types from a stub library (in this case `boto3-stubs`), or custom annotated types that can be checked with `beartype`.\n\n## Installation/Use\n\nSee the [list of services](services.md) to see what is currently implemented.\n\n### Supported python versions:\n- `>= 3.7`\n\nInstall with `pip`:\n\n`pip3 install bearboto3`\n\nor with whatever dependency management tool you use (like [`poetry`](https://python-poetry.org/)):\n\n`poetry add bearboto3`\n\nThen in your code, import the specific types you need:\n\n```python\nfrom beartype import beartype\nfrom bearboto3.s3 import S3Client, Bucket\nimport boto3\n\n@beartype\ndef example(s3: S3Client) -> Bucket:\n    return s3.create_bucket(Bucket='mybucket')\n\ns3_client = boto3.client('s3')\nbucket = example(s3_client)\n```\n\nYou will be able to have your salmon and eat it too!\n\n## Installing the type stubs\nAt present, there does not appear to be a way in `pyproject.toml` to specify extra/optional packages that should be installed as _dev_ dependencies. The type stubs for each service (which allow for IDE integration courtsey of [boto3-stubs](https://pypi.org/project/boto3-stubs/)) can be installed as extras such as:\n\n`poetry install bearboto3[s3]`\n\nbut **NOTE** this will install the type stubs as _runtime_ dependencies given the limitations above. The type stub libraries are _not_ needed to run any code you use this package with, so the recommended approach is to install whatever type stubs you need yourself in your project's `dev-dependencies` section.\n\nFuture work includes being able to isolate installing `bearboto3` runtime type definitions per service, like you are able to specify with `moto` and `boto3-stubs`.\n\n## Contributing\n\nSee [contributing](contributing.md)\n\n## Acknowledgements\n\n* @leycec For being an avid supporter and welcoming me to the `beartype` family",
    'author': 'Paul Hutchings',
    'author_email': 'dev@studiop.page',
    'maintainer': 'Paul Hutchings',
    'maintainer_email': 'dev@studiop.page',
    'url': 'https://github.com/beartype/bearboto3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
