# FractAlgebra
A simple fraction calculator CLI

## Features
* Accepts arbitrarily many fractions, not just two at a time
* returns the answer in lowest common denominator

## Installing

 ### Using `pipx` (simple and quick 🚀)
 I have [published fractalgebra as a PyPi package](https://pypi.org/project/fractalgebra/),
 _so you don't have to pull this repo to use the CLI_. Even better, using
 [pipx](https://github.com/pypa/pipx#pipx--install-and-run-python-applications-in-isolated-environments),
 you can jump in and begin adding fractions without worrying about your python environment.
 
 1. Follow the [instructions to install pipx](https://pypa.github.io/pipx/installation/) on your system 
 2. ```bash
    > pipx install fractalgebra
        installed package fractalgebra 0.1.1, installed using Python 3.9.7
        These apps are now globally available
        - fa
        done! ✨ 🌟 ✨
    > fa 1/2 + -3_3/2
      =  -4
    
### Build From Source
1. Python 3.9 or greater is required. Install it [here](https://www.python.org/downloads/), or use
your Python env manager of choice (I prefer [Conda](https://conda.io/projects/conda/en/latest/index.html))
2. This project uses [Poetry](https://python-poetry.org/docs/#installation) for dependency management and packaging
3. ```bash 
    > git clone git@github.com:bookRa/fractalgebra.git
    ...
    > cd fractalgebra
    > poetry install
    ...
    > fa -1/2 + -3/2
        = -2
    ```


### `TODO:` Downloadable Binary
 > time-permitting, I would use a tool like [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html)
in combination with GitHub Actions to publish an executable or zip/folder (to the Releases Page)
which any user can simply drop into their file system begin using fractalgebra without relying on any external tooling (including Python).


## Testing
1. Follow the same instructions above for `"Build From Source"`
2. ```bash
    > poetry run pytest                                                                                            
    Test session starts (platform: linux, Python 3.9.7, pytest 7.0.1, pytest-sugar 0.9.4)
    ...
    tests/fractalgebra_test.py ✓                                          4% ▌
    tests/helpers_test.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓                                 65% ██████▌
    tests/main_test.py ✓✓✓✓✓✓✓✓                                         100% ██████████

    Results (0.33s):
        23 passed
    ```

## Usage

1. Provide a space-delimeted math string using rational numbers and math operators to the `fa` command
    * A rational number can be a whole number (`3`), a fraction  a mixed fraction formatted with an
    underscore (`3_3/4`) or a fraction (`-9/4`).
    * Negative signs are allowed anywhere 
    __except on the fraction part of a mixed fraction__. Mathematically, this is ambiguous
    (at least based on my research)
    * The only math operations currently supported are add (`+`), subtract (`-`),
     multiply (`*`), and divide(`/`) 