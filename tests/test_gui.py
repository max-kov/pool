import subprocess
import time


def test_gui1():
    subprocess.run(["xvfb-run", "python", "../main.py", "--nomenu"])
    time.sleep(3)
    subprocess.run(["xdotool", "key", "enter"])


def test_gui2():
    subprocess.run(["xvfb-run", "python", "../main.py", "--badoption"])
