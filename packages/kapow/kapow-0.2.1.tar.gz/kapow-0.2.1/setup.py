# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kapow',
 'kapow.cli',
 'kapow.cli.resources',
 'kapow.handlers',
 'kapow.handlers.argparse',
 'kapow.handlers.core',
 'kapow.handlers.docopt',
 'kapow.resources']

package_data = \
{'': ['*']}

install_requires = \
['docopt-ng>=0.7.2,<0.8.0', 'rich>=11.2.0,<12.0.0', 'tomlkit>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['kapow = kapow.cli:main']}

setup_kwargs = {
    'name': 'kapow',
    'version': '0.2.1',
    'description': '',
    'long_description': '# kapow\n\n\nA python application launch framework with a punch! Kapow!\n\n**Warning**: This alpha software currently under active development\n\n\n## Installation\n\n```bash\npip install kapow\n```\n\n\n```bash\npoetry add kapow\n```\n\n`kapow` is a simple framework for coordinating the various pieces \nrequired to launch a python application. Parsing command line arguments,\nreading configurations, setting up logging, deciding where those resources \nlive, validating inputs are all pieces of the puzzle when an application\nstarts. `kapow` tries to make this process easier by providing a simple\npipline, builtin handlers and a few default setups to choose from - all while\nallowing the user to customize for their particular use case. \n\n\n## kapow cli\n\n`kapow` comes with a cli for generating a python application project. \nIt is also the easiest way for the user to learn how `kapow` applications\nwork.\n\n\n### The Basic Project\n\n*Show an example of creqting the default basic project.*\n\n\n### The Advanced Project\n\n*Show an example of creating the default advanced project.*\n\n\n\n\n\n',
    'author': 'Mark Gemmill',
    'author_email': 'mark@markgemmill.com',
    'maintainer': 'Mark Gemmill',
    'maintainer_email': 'dev@markgemmill.com',
    'url': 'https://github.com/markgemmill/kapow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
