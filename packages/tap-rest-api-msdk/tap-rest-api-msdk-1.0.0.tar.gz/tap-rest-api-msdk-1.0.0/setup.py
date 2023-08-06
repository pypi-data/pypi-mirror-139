# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_rest_api_msdk']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.4.0,<2.0.0',
 'genson>=1.2.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.3.11,<0.4.0']

entry_points = \
{'console_scripts': ['tap-rest-api-msdk = '
                     'tap_rest_api_msdk.tap:TapRestApiMsdk.cli']}

setup_kwargs = {
    'name': 'tap-rest-api-msdk',
    'version': '1.0.0',
    'description': '`tap-rest-api-msdk` is a Singer tap for REST APIs, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Josh Lloyd',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Widen/tap-rest-api-msdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
