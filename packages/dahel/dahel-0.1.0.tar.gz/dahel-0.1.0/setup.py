# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['dahel']
install_requires = \
['ipykernel>=6.9.1,<7.0.0', 'pandas>=1.4.1,<2.0.0', 's3fs>=2022.2.0,<2023.0.0']

setup_kwargs = {
    'name': 'dahel',
    'version': '0.1.0',
    'description': 'Frequently used data helpers.',
    'long_description': None,
    'author': 'Fabian Gunzinger',
    'author_email': 'fa.gunzinger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
