# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsiconv']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'pytz>=2021.3,<2022.0']

entry_points = \
{'console_scripts': ['tsiconv = tsiconv.__main__:main']}

setup_kwargs = {
    'name': 'tsiconv',
    'version': '0.0.1',
    'description': 'Python Boilerplate contains all the boilerplate you need to create a Python package.',
    'long_description': '# tsiconv\n\ntsiconv is a cli tool I created to take an input time and convert to UTC (optionally a destination timezone).\n\nMany tools I ran accross log in UTC time. Additionally SOC\'s are now run by people in different timezones including PST, MST, EST, CST, or international timezones in Africa, India, Europe, Asia.0\n\n# Installation\nI highly recommend you use `pipx` to install this, as it creates the virtualenv for you and seamlessly handles the loading of the virtual environment when running this tool. If you choose not to use `pipx`, you should create a virtualenv and possibly a wrapper script to launch this in the virtualenv.\n\n```sh\npipx install tsiconv\n```\n\n# Usage\n\nThe following is the help for the program\n```\nusage: __main__.py [-h] [-V] [-v] -t TIME [-s SOURCE] [-d DESTINATION] [-l]\n\n a program to convert timezones\n    ex: python tsiconv.py\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -V, --version         show program\'s version number and exit\n  -v, --verbose\n  -t TIME, --time TIME  A datetime to convert. This should be in ISO-8601 format\n  -s SOURCE, --source SOURCE\n                        A source timezone to translate from. Only required if --time is a naive format\n  -d DESTINATION, --destination DESTINATION\n                        A destination timezone to translate from\n  -l, --list            List out the timezones supported by this application\n```\n\nWithout providing a destination timeformat, the default is to convert to UTC.\n\n# Examples\n\n```sh\n# print help/usage\ntsiconv -h\n\n# print all available timezone formats\ntsiconv -l\n\n# Convert from Central European Time to Eastern Standard Time\ntsiconv -t "2011-12-03T10:15:30+01:00" -d America/New_York\n\n# Convert from Central Standard Time to Eastern Standard Time\ntsiconv -t "2011-12-03T10:15:30" -s America/Chicago -d America/New_York\n\n# Convert to UTC verbosely\ntsiconv -v -t "2011-12-03T10:15:30+05:00"\n```\n\n# Credits\n\nThis package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tbennett6421/pythoncookie](https://github.com/tbennett6421/pythoncookie) project template.\n',
    'author': 'Tyler Bennett',
    'author_email': 'tbennett6421@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tbennett6421/tsiconv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
