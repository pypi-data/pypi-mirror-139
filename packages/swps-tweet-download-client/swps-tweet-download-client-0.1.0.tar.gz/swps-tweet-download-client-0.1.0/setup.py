# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swps_tweet_download_client',
 'swps_tweet_download_client.application',
 'swps_tweet_download_client.domain']

package_data = \
{'': ['*']}

install_requires = \
['XlsxWriter>=3.0.2,<4.0.0',
 'arrow>=1.2.2,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'dynaconf>=3.1.7,<4.0.0',
 'minio>=7.1.2,<8.0.0',
 'pandas>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['tweet_download = swps_tweet_download_client.main:main']}

setup_kwargs = {
    'name': 'swps-tweet-download-client',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Marcin Wątroba',
    'author_email': 'markowanga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
