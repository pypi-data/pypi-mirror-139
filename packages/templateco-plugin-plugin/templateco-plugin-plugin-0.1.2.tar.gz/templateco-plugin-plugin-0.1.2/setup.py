# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['templateco_plugin_plugin']

package_data = \
{'': ['*'],
 'templateco_plugin_plugin': ['dist/*',
                              'poetry/*',
                              'template/*',
                              'template/{% if use_subfolder %}{{ prefix }}_{{ '
                              'name }}_plugin/*',
                              'template/{% if use_subfolder %}{{ prefix }}_{{ '
                              'name }}_plugin/{% endif %}template/*',
                              'tooling/*']}

install_requires = \
['templateco>=0,<1']

setup_kwargs = {
    'name': 'templateco-plugin-plugin',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Mike Gregory',
    'author_email': 'mike.ja.gregory@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
