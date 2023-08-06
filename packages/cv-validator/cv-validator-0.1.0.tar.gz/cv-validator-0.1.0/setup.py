# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cv_validator',
 'cv_validator.checks',
 'cv_validator.checks.data',
 'cv_validator.checks.metric',
 'cv_validator.core',
 'cv_validator.utils']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.0.1,<9.0.0',
 'ipywidgets>=7.6.5,<8.0.0',
 'numpy>=1.22.1,<2.0.0',
 'onnx>=1.11.0,<2.0.0',
 'onnxruntime>=1.10.0,<2.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'pandas>=1.4.0,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'px>=0.1.0,<0.2.0',
 'scipy>=1.8.0,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'cv-validator',
    'version': '0.1.0',
    'description': 'Tool for validating your computer vision data and model results.',
    'long_description': '[//]: # (<p align="center">)\n\n[//]: # (<a href="https://github.com/ningeen/ml-validator/actions?query=workflow%3ATest" target="_blank">)\n\n[//]: # (    <img src="https://github.com/ningeen/ml-validator/workflows/Test/badge.svg" alt="Test">)\n\n[//]: # (</a>)\n\n[//]: # (<a href="https://github.com/ningeen/ml-validator/actions?query=workflow%3APublish" target="_blank">)\n\n[//]: # (    <img src="https://github.com/ningeen/ml-validator/workflows/Publish/badge.svg" alt="Publish">)\n\n[//]: # (</a>)\n\n[//]: # (<a href="https://codecov.io/gh/ningeen/ml-validator" target="_blank">)\n\n[//]: # (    <img src="https://img.shields.io/codecov/c/github/ningeen/ml-validator?color=%2334D058" alt="Coverage">)\n\n[//]: # (</a>)\n\n[//]: # (<a href="https://pypi.org/project/cv-validator" target="_blank">)\n\n[//]: # (    <img src="https://img.shields.io/pypi/v/typer?color=%2334D058&label=pypi%20package" alt="Package version">)\n\n[//]: # (</a>)\n\n[//]: # (</p>)\n\n# CV validator\nLibrary to validate computer vision data and models.\n',
    'author': 'Ruslan Sakaev',
    'author_email': 'sakaevruslan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ningeen/cv-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
