# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_link']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0', 'slam-cli>=1.0.0,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['link-command = poetry_link:LinkCommandPlugin']}

setup_kwargs = {
    'name': 'poetry-link',
    'version': '0.1.6',
    'description': 'Editable installs for packages developed with Poetry using Flit.',
    'long_description': "# poetry-link\n\nPoetry natively does not support editable installs (as of writing this on Jan 22, 2022). This\ncommand makes use of the Flit backend to leverage its excellent symlink support. Relevant parts of\nthe Poetry configuration will by adpated such that no Flit related configuration needs to be added\nto `pyproject.toml`.\n\nThis package depends on [Slam](https://pypi.org/project/slam-cli/) for the `slam link` command and\nexposes it as plugin in Poetry.\n\n### Example usage\n\n    $ poetry link\n    Discovered modules in /projects/my-package/src: my_package\n    Extras to install for deps 'all': {'.none'}\n    Symlinking src/my_package -> .venv/lib/python3.10/site-packages/my_package\n",
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
