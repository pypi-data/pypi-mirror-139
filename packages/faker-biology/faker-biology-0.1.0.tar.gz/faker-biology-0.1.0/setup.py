# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faker_biology',
 'faker_biology.providers',
 'faker_biology.providers.bioseq',
 'faker_biology.providers.celltypes',
 'faker_biology.providers.mol_biol',
 'faker_biology.providers.organs',
 'faker_biology.tests']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=12.3.0,<13.0.0', 'faker-python>=0.0.1,<0.0.2', 'unittest>=0.0,<0.1']

setup_kwargs = {
    'name': 'faker-biology',
    'version': '0.1.0',
    'description': 'Fake data from biology',
    'long_description': '# faker-biology\nBiology-related fake data provider for Python Faker\n\nSome providers for biology-related concepts and resources\n',
    'author': 'richard',
    'author_email': 'ra22597@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richarda23/faker-biology',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
