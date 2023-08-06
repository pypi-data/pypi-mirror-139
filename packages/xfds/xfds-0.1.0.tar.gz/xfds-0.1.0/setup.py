# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xfds']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0', 'requests>=2.27.1,<3.0.0', 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['xfds = xfds.core:main']}

setup_kwargs = {
    'name': 'xfds',
    'version': '0.1.0',
    'description': 'FDS Runner using openbcl/fds-dockerfiles',
    'long_description': "[![Tests](https://github.com/pbdtools/xfds/workflows/Tests/badge.svg)](https://github.com/pbdtools/xfds/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/pbdtools/xfds/branch/master/graph/badge.svg)](https://codecov.io/gh/pbdtools/xfds)\n[![PyPI](https://img.shields.io/pypi/v/xfds.svg)](https://pypi.org/project/xfds)\n\n# xFDS\n\nTool for executing FDS runs with [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles).\n\nDo you have FDS installed on your machine? Do you know where the FDS executable is located? Do you know what version it is? If you installed FDS and Pathfinder, you might have multiple versions of FDS on your machine, but which one do you use?\n\nxFDS leverages the power of Docker to give you acess to all the versions of FDS without having to manage the different versions of FDS yourself. Best of all, you don't have to change or install anything when FDS has a new release!\n\nOnce xFDS is installed, all you have to do is navigate to your file and type `xfds`. It will locate the first FDS file in the directory and run it with the latest version of FDS!\n\n```\n~/tests/data/fds$ ls\ntest.fds\n~/tests/data/fds$ xfds\ndocker run --rm --name test-1b6d0d27-2cce-4555-a827-4b31d0e03215 -v /tests/data/fds:/workdir openbcl/fds:6.7.7 fds test.fds\n```\n\n## Usage\n\nxfds [options] [fds_file]\n\n### Options\n- `-h`, `--help`: Display help dialogue\n- `-i`, `--interactive`: Launch Docker container in interactive mode (`--it`). By default, the Docker image will run the FDS model, but interactive mode will put you into the container where you can start the FDS model manually. This is good for when you are rapidly iterating and don't want to wait for the Docker image load time.\n- `-v`, `--version`: Specify FDS version to use. The FDS version can also be extracted from the file path or metadata in the FDS file.\n- `-n`, `--processors`: Specify number of processors. Defaults to 1 processor. If the number of processors is greater than 1, it will invoke MPI for you (`mpiexec -n #`). Ignored if interactive mode is enabled.\n- `--fds-versions`: List FDS versions available on Docker Hub and exit. See [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles) for compatability information.\n\n### Arguments:\n- `fds_file`: The FDS file or directory to run.\n  - If a **FDS file** is specified, the FDS model will run.\n  - If a **directory** is specified, xFDS will find the first FDS file in the directory and assume that is what it should run. If no fds file exists, xFDS will default to interactive mode.\n  - if **nothing** is specified, the current directory is used and the above rules are applied.\n\n## Features\n\n**Auto-detect FDS file in directory**\n\nIf you're in a directory containing an FDS file, xFDS will find the FDS file without you specifying what file to run. This is best when each FDS model has its own directory. If multiple FDS files are in the directory, only the first file found will be executed.\n\nIf no FDS file is found, xFDS will put you into an interactive session with the directory mounted inside the Docker container. If no directory is specified, the current working directory will be used.\n\n**Latest version of FDS always available.**\n\nxFDS will always default to the latest version thanks to how the Docker images are created, but you're always welcome to use an older version of FDS if needed. See [fds-dockerfiles](https://github.com/openbcl/fds-dockerfiles) for supported versions.\n\n**Always know what FDS version you're using.**\n\nxFDS will inject the FDS version into the container name so there's no question what version of FDS is running. xFSD will also append a globally unique ID so there's no conflicts in having multipe containers running.\n\n**Runs in Background**\n\nFire and forget. Unless you use the interactive mode, xFDS will run your model in a container and free up the terminal for you to keep working.\n\n## Installation\n\n### Prerequisites\nTo use xFDS, you must have the following installed on your workstation:\n\n- [Docker](https://www.docker.com/): Needed to run fds-dockerfiles images\n- [Python](https://www.python.org/): Needed to run pipx\n- [pipx](https://pypa.github.io/pipx/): Needed to install xFDS\n\nDocker will allow you to run any suported version of FDS without installing it on your machine.\n\npipx allows you to install and run Python applications in isolated environments. This means that xFDS will be available anywhere on your machine and will not interfere with other Python projects or installations.\n\n### Install xFDS\nOnce Docker, Python, and pipx are installed, install xFDS with the following command:\n\n```\npipx install xfds\n```\n\n## License\n\nxFDS is licensed under the [MIT License](https://opensource.org/licenses/MIT). FDS is public domain and fds-dockerfiles is released under the MIT License. Since this is a light wrapper for both projects, it only seems appropriate to release xFDS for public use.\n",
    'author': 'Brian Cohan',
    'author_email': 'briancohan@pbd.tools',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pbdtools/xfds',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
