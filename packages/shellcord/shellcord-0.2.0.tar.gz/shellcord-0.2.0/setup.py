# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shellcord']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'flake8>=4.0.1,<5.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.0.1,<8.0.0']

entry_points = \
{'console_scripts': ['shellcord = shellcord.cli:cli']}

setup_kwargs = {
    'name': 'shellcord',
    'version': '0.2.0',
    'description': 'Easily create runbooks from your shell commands',
    'long_description': "# Shellcord\nGenerate runbooks and READMEs from your shell sessions.\n\n\n\n\n## Installation\n\n## Usage\n\n\n## Supported platforms\nNote that this tool is in alpha and still not thoroughly tested on shells/platforms besides the following:\n### Python\n* 3.7\n* 3.9\n### Operating systems\n* Linux `5.11.0-49-generic x86_64 GNU/Linux `\n\n### Shells\nConfirmed working in:\n* zsh: `zsh 5.8 (x86_64-ubuntu-linux-gnu)`\n* bash: `GNU bash, version 5.1.4(1)-release (x86_64-pc-linux-gnu)`\n\n\n\n### Limitations\nIdeally, this tool would be a simple invocation of [script](https://man7.org/linux/man-pages/man1/script.1.html) with some logic to generate a runbook from that typescript file. However, given that `script` only uses a psuedo-terminal, getting the exit code is non-trivial without basically making your own shell. So we do the next best thing and use each individual shells `precmd/PROMPT_COMMAND` instead. \n\nCurrently, shellcord collects:\n* The command being run\n* The exit code of that command\n\nIdeally though, it would also be able to get stdout so the generated runbook has example output.\n\n## Development\nThis tool is currently under development and any support is more than welcome, especially if you want to get shellcord working in your shell of choice.\n\nPlease cut issues as you see fit based on usage and feel free to send pull-requests.\n\n### Testing \nRun the tests `poetry run python3 -m pytest`\n\n\n\n### How it works\nShellcord works by modifying the shell's `precmd/PROMP_COMMAND` or whatever equivalent with our own function which will:\n* Generate a unique id for each command\n* Get the exit code of the last command run\n* Get the actual command which was run last\n* Dump all that data to a `scord-log` file\n\nOnce all the command data has been collected, shellcord will then use the `scord-log` file to generate a runbook based on the parameters selected.\n\n\n### Components\n* init.sh: Used to setup a scord session and modify precmd\n* de-init.sh: Used to close the session and undo all the precmd work \n* shellcord.py: Used to generate runbooks and tag commands",
    'author': 'Ben',
    'author_email': 'bnichs55@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bnichs/shellcord.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
