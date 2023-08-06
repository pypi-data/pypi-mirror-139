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
['ipython>=7.16.3',
 'ipywidgets>=7.6.5,<8.0.0',
 'joblib>=1.1.0,<2.0.0',
 'numpy>=1.19.5',
 'onnx>=1.11.0,<2.0.0',
 'onnxruntime>=1.9.0',
 'opencv-python>=4.5.2,<5.0.0',
 'pandas>=1.1.5',
 'plotly>=5.6.0,<6.0.0',
 'scipy>=1.5.4',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'cv-validator',
    'version': '0.1.4',
    'description': 'Tool for validating your computer vision data and model results.',
    'long_description': '<p align="center">\n<a href="https://pypi.org/project/cv-validator" target="_blank">\n    <img src="https://img.shields.io/pypi/v/cv-validator?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n</p>\n\n# CV validator\nLibrary to validate computer vision data and models.\n\n## Installation\n```commandline\npip install cv-validator\n```\n\n## Usage\nExample on colab: [Link](https://colab.research.google.com/drive/184BZS6iJJTtAyHMY34TOS-W-MjpiOqCW?usp=sharing)\n\n```python\nfrom cv_validator.checks import *\nfrom cv_validator.core.data import DataSource\nfrom cv_validator.core.suite import BaseSuite\n\n# Create class with data information\ntrain = DataSource(train_image_paths, train_labels, train_predictions, transform=None)\ntest = DataSource(test_image_paths, test_labels, test_predictions, transform=transform)\n\n# Create suite with different checks\nsuite = BaseSuite(\n    checks=[\n        ImageSize(),\n        ColorShift(),\n        BrightnessCheck(need_transformed_img=True),\n        ClassifierLabelDistribution(),\n        MetricCheck(),\n        MetricDiff(),\n        MetricBySize(),\n        MetricByRatio(),\n        HashDuplicates(mode="exact", datasource_type="train"),\n    ]\n)\n\n# Run checks\nsuite.run(task="multiclass", train=train, test=test, num_workers=4)\n```\n',
    'author': 'Ruslan Sakaev',
    'author_email': 'sakaevruslan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ningeen/cv-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
