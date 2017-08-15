<h1 align="center"> Pool </h1>
<p align="center">
    <a href="https://codeclimate.com/github/max-kov/pool">
        <img src="https://codeclimate.com/github/max-kov/pool/badges/gpa.svg"
             alt="CodeClimate">
    <a href="https://travis-ci.org/max-kov/pool">
        <img src="https://travis-ci.org/max-kov/pool.svg?branch=table_rework"
             alt="build status">
             </a> 
</p>

<p align="center"><b> A pool game written entirely in python! </b></p>


![Alt text](/../screenshots/poolgif.gif?raw=true "Game gif")


## Features
* Realistic collisions based on a two-dimensional Newtonian model.
* Simple configuration file (config.py) with many changeable options like ball size, ball colour, cue length/thickness and many more.
* Algorithms which render ball sprites using rotation matrices.
* Tests for collision functions and other math related functions.
* A small, but highly scalable game menu.

## Installing
### Dependencies
The pool game requires python 3.5 with modules [pygame](https://www.pygame.org/wiki/about), [numpy](http://www.numpy.org/) and [zope.event](https://docs.zope.org/zope.event/).

### Installing on most linux systems
Install python 3.5 with pip and venv.

```
sudo apt install python3.5 python-pip python-venv
```

Then, clone the github code and run the game using run.sh, which will setup a virtual python environment with the aforementioned modules.

```
git clone https://github.com/max-kov/pool
cd pool
./run.sh
```

### Windows

Download [python 3.5](https://www.python.org/downloads/release/python-353/), [zope.event](https://pypi.python.org/pypi/zope.event), [pygame](http://www.pygame.org/download.shtml), [numpy](https://sourceforge.net/projects/numpy/files/NumPy/) (often is included with python) and then download the program and run `main.py`.
Alternatively, [add python to the path variable](https://stackoverflow.com/a/4855685) and run `python -m pip install -r requirements.txt` in the *administrator* cmd in the game folder to install the dependencies.

## Running the tests

To run the tests we will require `pytest` module. To install it simply run

```
pip install pytest
```

To run the tests write `PYTHONPATH=./pool py.test` in the game folder. Pytest will recursively search for test files (which are initially located in tests folder).
You can also check test coverage by installing `pip install pytest-coverage` and executing
`pytest --cov=.` in the pool folder. That will analyse which files and which lines of code are being tested by the tests.
`.coveragerc` will prevent the module from analysing test files as well.

## Built With

* [Python 3.5](https://www.python.org/)
* [Pygame](http://www.pygame.org/) - 2d graphics library
* [Numpy](http://www.numpy.org/) - Scientific computing library, used here for vector opertations
* [Travis CI](https://travis-ci.org/) and [CodeClimate](https://codeclimate.com/) - Testing and code analysis
