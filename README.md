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
* A small and configurable game menu.

## Installing
### Dependencies
The pool game requires python 3.5 with modules which are listed in `requirements.txt` .

### Installing on debian-based linux distributions
Install python 3.5 with pip and venv.
```
sudo apt install python3.5 python3-pip python3-venv
```
Then, clone the github code and run the game using run.sh, which will setup a virtual python environment with the aforementioned modules.
```
git clone https://github.com/max-kov/pool
cd pool
./run.sh
```

### Windows

Download [python 3.5](https://www.python.org/downloads/release/python-353/) with [pip](https://docs.python.org/3/installing/index.html#pip-not-installed) then [add python to the path variable](https://superuser.com/a/143121) and run
```
python3 -m pip install -r requirements.txt
```
in the *administrator* cmd in the game folder to install the dependencies. Finally, start `main.py` to run the game.

## Running the tests

To run the tests we will need extra modules. Run
```
pip3 install -r test_requirements.txt
```
in the game folder to install the testing modules. To run the tests write
```
PYTHONPATH=./pool pytest tests/
```
You can also check test coverage by executing
```
PYTHONPATH=./pool pytest --cov=. tests/
```
That will analyse which files and which lines of code were executed by the tests.
`.coveragerc` will prevent the module from analysing test files as well.

## Built With

* [Python 3.5](https://www.python.org/)
* [Pygame](http://www.pygame.org/) - 2d graphics library
* [Numpy](http://www.numpy.org/) - Scientific computing library, used here for vector opertations
* [Travis CI](https://travis-ci.org/max-kov/pool) and [CodeClimate](https://codeclimate.com/github/max-kov/pool) - Testing and code analysis
