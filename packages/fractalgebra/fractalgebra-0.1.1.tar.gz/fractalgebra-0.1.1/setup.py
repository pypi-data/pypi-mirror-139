# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fractalgebra']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['fa = fractalgebra.main:calc']}

setup_kwargs = {
    'name': 'fractalgebra',
    'version': '0.1.1',
    'description': 'a simple fractions calculator',
    'long_description': '# FractAlgebra\nA simple fraction calculator CLI\n\n## Features\n* Accepts arbitrarily many fractions, not just two at a time\n* returns the answer in lowest common denominator\n\n## Installing\n\n ### Using `pipx` (simple and quick 🚀)\n [pipx](https://github.com/pypa/pipx#pipx--install-and-run-python-applications-in-isolated-environments) allows you to install (or just test out using the `run` command) python CLIs safely using Isolated Environments\n \n _Requires Python 3.6 or greater_\n\n ### Downloadable Binary (TODO)\n\n ### Build From Source\n\n## Usage\n\n## Development\n### Building the Project\n### Environment Setup',
    'author': 'bookRa',
    'author_email': 'omar.abdelbadie1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bookRa/fractalgebra',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
