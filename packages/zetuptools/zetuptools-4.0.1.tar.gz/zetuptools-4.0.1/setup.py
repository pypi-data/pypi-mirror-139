# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zetuptools']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.3,<6.0.0', 'dunamai>=1.8.0,<2.0.0', 'zmtools>=2.0.0']

entry_points = \
{'console_scripts': ['install-directives = zetuptools.__main__:_entry']}

setup_kwargs = {
    'name': 'zetuptools',
    'version': '4.0.1',
    'description': 'Useful for doing post-install/uninstall things',
    'long_description': '# `zetuptools`\n\n`zetuptools` contains a command line tool, `install-directives`, used to aid in post-install and post-uninstall steps for packages installed with `pip`. It also includes a class to represent packages installed with `pip`.\n\nIt originally had some other functions I considered useful in a `setup.py` file, but these have been scrapped as of version 3.0 as they cause too many dependecy confusions and honestly do not save that much time.\n\nAs of version 4.0, there are breaking changes regarding Docker images. You need to specify them, sorted, in the constructor of an `InstallDirectives` object.\n\n## Usage\n\nThe idea is to write a custom class that extends `InstallDirective`, overriding its `package_name` and `module_name` attributes and its `_install` and `_uninstall` functions. This should be placed in a Python package called `install_directives`.\n\nThese overridden functions will be called upon running the command line tool as such.\n\n```text\nusage: install-directives [-h] [--verbose] package {install,uninstall}\n\npositional arguments:\n  package\n  {install,uninstall}\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --verbose            be verbose\n```\n\nSee [`apt-repo`](https://github.com/zmarffy/apt-repo) for a real-world example of how to use this with your Python package. Note the placement of `install_directives` as well as the fact that the README mentions that you should run `install-directives apt-repo install` after the `pip` package is installed.\n\n`zetuptools` should be also helpful for building Docker images related to the project. There is a function called `build_docker_images` that will do just that. It attempts to build Docker images cleverly in the order in which they are needed to be built, but this could actually be coded wrong. Be advised. I will revisit this at some point in the future.\n\n`install-directives [package_name] uninstall` should be run *before* the uninstallation of the `pip` package. Similarly, a `remove_docker_images` function exists.\n',
    'author': 'Zeke Marffy',
    'author_email': 'zmarffy@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zmarffy/zetuptools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
