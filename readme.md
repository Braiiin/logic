#Braiiin Logic Tier

a RESTful API for basic CRUD operations, for now

##Developer Version


1. Make sure Python3, Pip, and Mongodb are installed.
1. Create new virtaulenv named "env" `python3 -m venv env`.
1. Launch virtualenv `source env/bin/activate`.
1. Create mongodb datastore `mkdir env/db`.
1. Install requirements `pip3 install -r requirements.txt`.
1. Launch datastore. `service mongodb start`.
1. Launch service. `python3 run.py`.

*For subsequent runs, after installation, you can use `source activate.sh`.*

## Developer Guidelines

###Docstrings

All docstrings should use one of the following two formats:

Minimal
```
"""Basic docstring for the method or class"""
```

Detailed
```
"""
One-liner description

Information
-----------
Basic information about usage

Detail
------
Optional section with clarifications that may not be needed

Example
-------
Sample Usage
"""
```

###Separatation of Purpose

Heed these guidelines when deciding where to put code.

- api.py : handling input/output for models, permissions by endpoint
- models.py : business logic

##Production Deployment

Assumes a non-root, sudo-capable user, deploying to Ubuntu 14.04

1. Update package index `sudo apt-get update`.
1. Upgrade everything `sudo apt-get upgrade`.
1. Install Apache2, MongoDB, Pip3, and Git `sudo apt-get install apache2 mongodb python3-pip git`.
1. Install Python3 WSGI `sudo apt-get install libapache2-mod-wsgi-py3`.
1. Make `python3` the default: `sudo rm /usr/bin/python; sudo ln -s /usr/bin/python3 /usr/bin/python`.
1. `cd` to `/var/www`.
1. Clone code `git clone https://.git`.
1. Disable multi-threading `sudo a2dismod mpm_event`.
1. Give Apache2 permission to run scripts `sudo a2enmod mpm_prefork cgi`.
1. Symlink configuration file for apache2 `sudo ln -s /var/www/logic/logic.conf /etc/apache2/sites-available/logic.conf`.
1. Activate the site `sudo a2ensite logic`.
1. Deactivate the default site `sudo a2dissite 000-default`.
1. `cd logic`
1. `source install.sh`
1. Launch the datastore `sudo service mongodb start`.
1. Restart server `sudo service apache2 reload`.