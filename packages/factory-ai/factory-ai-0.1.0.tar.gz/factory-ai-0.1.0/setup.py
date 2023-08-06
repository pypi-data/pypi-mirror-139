# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factory_ai']

package_data = \
{'': ['*']}

install_requires = \
['apache-beam>=2.35.0,<3.0.0',
 'bayesian-optimization>=1.2.0,<2.0.0',
 'future>=0.18.2,<0.19.0',
 'gekko>=1.0.2,<2.0.0',
 'gym>=0.21.0,<0.22.0',
 'keras-tuner>=1.1.0,<2.0.0',
 'keras==2.6',
 'matplotlib>=3.5.1,<4.0.0',
 'mediapipe>=0.8.9,<0.9.0',
 'opencv-python==4.4.0.46',
 'pyglet>=1.5.21,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'tensorflow-data-validation==1.4',
 'tensorflow-transform==1.4',
 'tensorflow==2.6']

setup_kwargs = {
    'name': 'factory-ai',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jidhu Mohan',
    'author_email': 'jidhu.mohan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
