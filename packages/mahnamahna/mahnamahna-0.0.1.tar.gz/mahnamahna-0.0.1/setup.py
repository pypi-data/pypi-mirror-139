# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mahnamahna', 'mahnamahna.voice']

package_data = \
{'': ['*']}

install_requires = \
['fifteen-ai>=0.2.2,<0.3.0',
 'gTTS>=2.2.3,<3.0.0',
 'playsound>=1.3.0,<2.0.0',
 'pyttsx3>=2.90,<3.0',
 'sounddevice>=0.4.4,<0.5.0',
 'vosk>=0.3.32,<0.4.0']

setup_kwargs = {
    'name': 'mahnamahna',
    'version': '0.0.1',
    'description': 'Media analysis',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
