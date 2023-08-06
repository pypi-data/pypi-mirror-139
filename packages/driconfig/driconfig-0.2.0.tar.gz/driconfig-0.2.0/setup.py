# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['driconfig']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<5.0']}

setup_kwargs = {
    'name': 'driconfig',
    'version': '0.2.0',
    'description': 'Pydantic-ish YAML configuration management.',
    'long_description': '<p style="text-align: center; padding-bottom: 1rem;">\n    <a href="https://dribia.github.io/driconfig">\n        <img \n            src="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png" \n            alt="driconfig" \n            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"\n        >\n    </a>\n</p>\n\n<p style="text-align: center">\n    <a href="https://github.com/dribia/driconfig/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/dribia/driconfig/workflows/Test/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/dribia/driconfig/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/dribia/driconfig/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://codecov.io/gh/dribia/driconfig" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/dribia/driconfig?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/driconfig" target="_blank">\n    <img src="https://img.shields.io/pypi/v/driconfig?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n</p>\n\n<p style="text-align: center;">\n    <em>A Pydantic-ish way to manage your project\'s YAML configurations.</em>\n</p>\n\n---\n\n**Documentation**: <a href="https://dribia.github.io/driconfig" target="_blank">https://dribia.github.io/driconfig</a>\n\n**Source Code**: <a href="https://github.com/dribia/driconfig" target="_blank">https://github.com/dribia/driconfig</a>\n\n---\n\nThe usage of YAML files to store configurations and parameters is widely accepted in the Python\ncommunity, especially in Data Science environments.\n\nDriConfig provides a clean interface between your Python code and these YAML configuration files.\n\nIt is heavily based on [Pydantic](https://pydantic-docs.helpmanual.io)\'s [Settings Management](https://pydantic-docs.helpmanual.io/usage/settings/),\npreserving its core functionalities and advantages.\n\n## Key features\n\n* Subclassing the `DriConfig` class we create an **interface to any YAML configuration file**.\n* Our project\'s **configurations are** then **attributes** of this class.\n* They are **automatically filled** with the values in the YAML configuration file.\n* We can define **complex configuration structures** using Pydantic models.\n* We preserve Pydantic\'s **type casting and validation**!\n\n## Example\nLet\'s say we have a YAML configuration file `config.yaml` with the following data:\n```yaml\n# config.yaml\nmodel_parameters:\n  eta: 0.2\n  gamma: 2\n  lambda: 1\n\ndate_interval:\n  start: 2021-01-01\n  end: 2021-12-31\n```\nThen we can parse with `driconfig` as follows:\n```python\nfrom datetime import date\nfrom typing import Dict\n\nfrom driconfig import DriConfig\nfrom pydantic import BaseModel\n\n\nclass DateInterval(BaseModel):\n  """Model for the `date_interval` configuration."""\n  start: date\n  end: date\n\n  \nclass AppConfig(DriConfig):\n   """Interface for the config/config.yaml file."""\n\n   class Config:\n       """Configure the YAML file location."""\n\n       config_folder = "."\n       config_file_name = "config.yaml"\n\n   model_parameters: Dict[str, float]\n   date_interval: DateInterval\n\nconfig = AppConfig()\nprint(config.json(indent=4))\n"""\n{\n    "model_parameters": {\n        "eta": 0.2,\n        "gamma": 2.0,\n        "lambda": 1.0\n    },\n    "date_interval": {\n        "start": "2021-01-01",\n        "end": "2021-12-31"\n    }\n}\n"""\n```\n',
    'author': 'Dribia Data Research',
    'author_email': 'info@dribia.com',
    'maintainer': 'Irene Pérez',
    'maintainer_email': 'irene@dribia.com',
    'url': 'https://dribia.github.io/driconfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
