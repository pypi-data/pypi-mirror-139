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
    'version': '0.1.3',
    'description': 'a simple fractions calculator',
    'long_description': '# FractAlgebra\nA simple fraction calculator CLI\n\n## Features\n* Accepts arbitrarily many fractions, not just two at a time\n* returns the answer in lowest common denominator\n\n## Installing\n\n ### Using `pipx` (simple and quick 🚀)\n I have [published fractalgebra as a PyPi package](https://pypi.org/project/fractalgebra/),\n _so you don\'t have to pull this repo to use the CLI_. Even better, using\n [pipx](https://github.com/pypa/pipx#pipx--install-and-run-python-applications-in-isolated-environments),\n you can jump in and begin adding fractions without worrying about your python environment.\n \n 1. Follow the [instructions to install pipx](https://pypa.github.io/pipx/installation/) on your system \n 2. ```bash\n    > pipx install fractalgebra\n        installed package fractalgebra 0.1.1, installed using Python 3.9.7\n        These apps are now globally available\n        - fa\n        done! ✨ 🌟 ✨\n    > fa 1/2 + -3_3/2\n      =  -4\n    \n### Build From Source\n1. Python 3.9 or greater is required. Install it [here](https://www.python.org/downloads/), or use\nyour Python env manager of choice (I prefer [Conda](https://conda.io/projects/conda/en/latest/index.html))\n2. This project uses [Poetry](https://python-poetry.org/docs/#installation) for dependency management and packaging\n3. ```bash \n    > git clone git@github.com:bookRa/fractalgebra.git\n    ...\n    > cd fractalgebra\n    > poetry install\n    ...\n    > fa -1/2 + -3/2\n        = -2\n    ```\n\n\n### `TODO:` Downloadable Binary\n > time-permitting, I would use a tool like [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html)\nin combination with GitHub Actions to publish an executable or zip/folder (to the Releases Page)\nwhich any user can simply drop into their file system begin using fractalgebra without relying on any external tooling (including Python).\n\n\n## Testing\n1. Follow the same instructions above for `"Build From Source"`\n2. ```bash\n    > poetry run pytest                                                                                            \n    Test session starts (platform: linux, Python 3.9.7, pytest 7.0.1, pytest-sugar 0.9.4)\n    ...\n    tests/fractalgebra_test.py ✓                                          4% ▌\n    tests/helpers_test.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓                                 65% ██████▌\n    tests/main_test.py ✓✓✓✓✓✓✓✓                                         100% ██████████\n\n    Results (0.33s):\n        23 passed\n    ```\n\n## Usage\n\n1. Provide a space-delimeted math string using rational numbers and math operators to the `fa` command\n    * A rational number can be a whole number (`3`), a fraction  a mixed fraction formatted with an\n    underscore (`3_3/4`) or a fraction (`-9/4`).\n    * Negative signs are allowed anywhere \n    __except on the fraction part of a mixed fraction__. Mathematically, this is ambiguous\n    (at least based on my research)\n    * The only math operations currently supported are add (`+`), subtract (`-`),\n     multiply (`*`), and divide(`/`) ',
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
