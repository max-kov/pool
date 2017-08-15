#!/bin/bash
if !(command -v python3 > /dev/null 2>&1;) then
    echo python3 was not found on your system
    echo please check README.md for instructions
else
    if !(python3 -c "import venv" &> /dev/null;) then
        echo no venv module was found in python3
        echo please check README.md for instructions
    elif !(python3 -c "import pip" &> /dev/null;) then
        echo no pip module was found in python3
        echo please check README.md for instructions
    else
        if [ -e pool/bin/activate ]; then
            source pool/bin/activate
        else
            python3 -m venv pool
            source pool/bin/activate
            echo installing venv packages
            python3 -m pip install -r requirements.txt
            echo Succesfully installed a virtual environment.
        fi
        python3 pool/main.py
        deactivate
    fi
fi
