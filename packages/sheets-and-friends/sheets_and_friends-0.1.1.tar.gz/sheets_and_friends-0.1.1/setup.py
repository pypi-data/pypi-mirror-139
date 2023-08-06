# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheets_and_friends', 'sheets_and_friends.converters']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'click_log',
 'dpath>=2.0.6,<3.0.0',
 'glom>=22.1.0,<23.0.0',
 'hident>=0.1.7,<0.2.0',
 'pandasql>=0.7.3,<0.8.0',
 'pygsheets>=2.0.5,<3.0.0',
 'schemasheets>=0.1.7,<0.2.0']

entry_points = \
{'console_scripts': ['compare_enums = '
                     'sheets_and_friends.compare_enums:compare_enums',
                     'do_shuttle = sheets_and_friends.shuttle:do_shuttle',
                     'linkml2dataharmonizer = '
                     'sheets_and_friends.converters.commands:linkml2dataharmonizer',
                     'mod_by_path = sheets_and_friends.mod_by_path:mod_by_path',
                     'promote_to_select = '
                     'sheets_and_friends.converters.commands:promote_to_select']}

setup_kwargs = {
    'name': 'sheets-and-friends',
    'version': '0.1.1',
    'description': 'Create a LinkML model with as-is imported slots, imported but modified slots (via yq), or newly minted slots (via schemasheets)',
    'long_description': None,
    'author': 'Mark Andrew Miller',
    'author_email': 'MAM@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
