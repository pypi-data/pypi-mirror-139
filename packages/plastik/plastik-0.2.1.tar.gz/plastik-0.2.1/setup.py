# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plastik']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'matplotlib>=3.5.0,<4.0.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'plastik',
    'version': '0.2.1',
    'description': 'plastic surgery for plt',
    'long_description': 'None',
    'author': 'engeir',
    'author_email': 'eirroleng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
