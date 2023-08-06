# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioworkers_mongo']

package_data = \
{'': ['*']}

install_requires = \
['aioworkers>=0.15', 'motor>=1.3,<2.0']

setup_kwargs = {
    'name': 'aioworkers-mongo',
    'version': '0.1.0',
    'description': 'Module for working with MongoDB via asyncpg',
    'long_description': "# aioworkers-mongo\n\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aioworkers/aioworkers-mongo/CI)](https://github.com/aioworkers/aioworkers-mongo/actions?query=workflow%3ACI)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-mongo)](https://pypi.org/project/aioworkers-mongo)\n[![PyPI](https://img.shields.io/pypi/v/aioworkers-mongo)](https://pypi.org/project/aioworkers-mongo)\n\nMongo plugin for `aioworkers`.\n\n\n## Usage\n\n### Connection\n\nAdd this to aioworkers config.yaml:\n\n```yaml\nmongo:\n    cls: aioworkers_mongo.base.Connector\n    uri: 'mongodb://localhost:27017/'\n```\n\nYou can get access to mongo anywhere via context:\n\n```python\ndocs = [doc async for doc in context.mongo.db.collection.find({})]\n```\n\n## Development\n\nRun Mongo DB:\n\n```shell\ndocker run --rm -p 27017:27017 --name mongo -d mongo\n```\n\nInstall dev requirements:\n\n```shell\npoetry install\n```\n\nActivate env:\n\n```shell\n. .venv/bin/activate\n```\n\n\nRun tests:\n\n```shell\npytest\n```\n",
    'author': 'Alexander Bogushov',
    'author_email': 'abogushov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aioworkers/aioworkers-mongo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.11',
}


setup(**setup_kwargs)
