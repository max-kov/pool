#!/bin/bash
echo installing python3.5
sudo apt-get install python3.5 
sudo apt-get install python3-pip 
echo installing venv
python3.5 -m pip install virtualenv
virtualenv -p /usr/bin/python3.5 pool
source pool/bin/activate
echo installing venv packages
python3.5 -m pip install -r requirements.txt
deactivate
echo Succesfully installed a virtual environment.
echo Run ./run.sh to start the game.
