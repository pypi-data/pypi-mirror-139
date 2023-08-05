# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video_to_text_vtt']

package_data = \
{'': ['*']}

install_requires = \
['SpeechRecognition>=3.8.1,<4.0.0', 'moviepy>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['vtt_run = video_to_text.__main__:main']}

setup_kwargs = {
    'name': 'video-to-text-vtt',
    'version': '0.1.0',
    'description': 'Converts audio from movies to text',
    'long_description': None,
    'author': 'Mohammad Reza Maleki',
    'author_email': 'm.mlk9928@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
