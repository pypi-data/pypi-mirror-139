# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_workon']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0']

entry_points = \
{'console_scripts': ['gw = git_workon.cli:main']}

setup_kwargs = {
    'name': 'git-workon',
    'version': '2.0.0',
    'description': 'Utility that automates projects clone/remove and checks for nonpushed changes on removal',
    'long_description': '[![tests](https://github.com/ReturnedVoid/workon/actions/workflows/ci.yml/badge.svg)](https://github.com/ReturnedVoid/workon)\n\n# GIT workon\n\nDo you often need to clone some project, solve one task and remove it from your filesystem?\n\nAre you often afraid that you might leave something unpushed or stashed?\n\nDo you like to leave a perfectly clean desk after your work is done?\n\nThen this script is for you.\n\n## Installation\n\nThe package is available on `PyPi` and can be installed with `pip`:\n\n```bash\npip install git-workon\n```\n\n## Usage\n\n## Configuration\n\nThe script commands can be fully controlled by CLI arguments, but it is much convenient to have a configuration file\ndefining most of parameters. There is a special `config` command that will help you to prepare suitable configuration.\n\n```bash\ngw config [options]\n```\n\nThis command will:\n\n* Create configuration directory if it does not exist. It will use OS-specific config directory, e.g.\n  `~/.config/git_workon` for Linux\n* Copy template configuration file to the configuration directory if it does not exist\n\nThe configuration file is a simple JSON contains the following parameters:\n\n* `sources` - the array of sources from which projects will be cloned. Clone attempts will be done sequentially.\n  Example:\n\n  ```json\n  "sources": [\n    "https://github.com/<my_username>",\n    "git@github.com:<my_username>"\n  ]\n  ```\n\n  May be overridden by `-s/--source` argument. You can also define multiple sources: `-s first second -s third`\n* `dir` - the working directory. All projects will be cloned to this directory. May be overridden by `-d/--directory`\n  argument. `~` in path is supported\n* `editor` - the editor used to open a cloned project or the configuration. May be overridden by `-e/--editor` argument.\n  If not specified and `-e/--editor` argument is not provided, the script will try to use the editor specified by\n  `$EDITOR` environment variable. If that variable is not set, the script will try `vi` and `vim` consequently\n\nConfiguration example:\n\n```json\n{\n  "dir": "~/git_workon",\n  "editor": "vim",\n  "sources": [\n    "https://github.com/pallets",\n    "https://github.com/pypa"\n  ]\n}\n```\n\n### Start to work on a project\n\nWhen it is time to work on some project, use the `start` command:\n\n```bash\ngw start <my_project> [options]\n```\n\nThis command will:\n\n* If the project with a given name already exists in the working directory:\n  * open it with a configured editor\n* If the project with a given name does not exist:\n  * clone it from git sources into the working directory\n  * open the project with a configured editor\n\nSee `gw start --help` for other available options on how to control the command.\n\n### Finish your work with a project\n\nWhen you are done with your work, use `done` command:\n\n```bash\ngw done [<my_project>] [options]\n```\n\nThis command will:\n\n* Check for left stashes\n* Check for unpushed commits\n* Check for left unstaged changes\n* Check for unpushed tags\n* If anything from above was not pushed:\n  * fail with an error describing what was left unpushed\n* If everything was pushed:\n  * remove a project from the working directory\n\nIf a project name was not passed, the command will try to remove everything from the working directory (still,\nfolders containing ".git" will be checked for unpushed entities).\n\nSee `gw done --help` for other available options on how to control the command.\n\n## Bash completions\n\nImplemented as a bash script `workon_completions`. Currently, it adds completions only for basic commands.\nTo enable completions, simply copy the script to `/etc/bash_completion.d/` or copy it anywhere and source when you\nneed.\n',
    'author': 'Andrey Nechaev',
    'author_email': 'andrewnech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ReturnedVoid/workon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
