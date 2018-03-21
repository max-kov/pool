<h1 align="center"> Pool </h1>
<p align="center">
    <a href="https://travis-ci.org/max-kov/pool">
        <img src="https://travis-ci.org/max-kov/pool.svg?branch=master"
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
Install python 3.5 with pip, venv and pygame dependencies
```
sudo apt-get build-dep python-pygame
sudo apt-get install python-dev python3 python3-pip python3-venv
```
Then, clone the github code and run the game using run.sh, which will setup a virtual python environment with the aforementioned modules.
```
git clone git://github.com/max-kov/pool.git
cd pool
./run.sh
```
If the pygame installation **fails**, it's most likely due to apt not having any URIs in sources.list file. To fix execute
```
sudo sed -i -- 's/#deb-src/deb-src/g' /etc/apt/sources.list && sudo sed -i -- 's/# deb-src/deb-src/g' /etc/apt/sources.list
sudo apt-get update
```
and run the installation procedure again.

### Windows

Download [python 3.5](https://www.python.org/downloads/release/python-353/) with [pip](https://docs.python.org/3/installing/index.html#pip-not-installed) then [add python to the path variable](https://superuser.com/a/143121) and run
```
python -m pip install -r requirements.txt
```
in the *administrator* cmd in the game folder to install the dependencies. Finally, start `main.py` to run the game. You might have to use `python3` instead of `python` depending if you have python2 installed. To check that you are using the right vesrion, write `python` in the console to see what version is used.

## Running the tests

You can always see the results of the latest build [here](https://travis-ci.org/max-kov/pool). If you want to run the tests yourself, we will need extra modules. (On linux) Run
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
That will analyse which files and which lines of code were executed by the tests.`.coveragerc` will prevent the module from analysing test files as well. 

## Built With

* [Python 3.5](https://www.python.org/)
* [Pygame](http://www.pygame.org/) - 2d graphics library
* [Numpy](http://www.numpy.org/) - Scientific computing library, used here for vector opertations
* [Travis CI](https://travis-ci.org/max-kov/pool) and [CodeClimate](https://codeclimate.com/github/max-kov/pool) - Testing and code analysis
