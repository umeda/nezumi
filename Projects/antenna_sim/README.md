### Antenna Simulation Using PyNEC
The Scripts here are based on examples in the PyNEC repo: https://github.com/tmolteno/python-necpp.

I wanted to add some comments to make the functions easier for me to use and to be able to scale and adjust various basic antenna configurations. 

To create the virtual environment in which to run the examples, do the following:

virtualenv .venv -p python3<br>
source .venv/bin/activate<br>
pip install -r requirements.txt<br>

If you have problems with any of the above steps, the libraries below may need to be installed.

sudo apt-get install virtualenv<br>
sudo apt-get install g++<br>
sudo apt-get install python3-dev<br>


![Radiation Pattern](radiation_pattern_146_MHz.png)
![VSWR](vswr_146_MHz.png)

