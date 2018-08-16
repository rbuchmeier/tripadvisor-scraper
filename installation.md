https://stackoverflow.com/questions/23842713/using-python-3-in-virtualenv

Install Project from Github:

`git clone https://github.com/mariomarine/tripadvisor-scraper/`

Install Prerequisites:

`sudo apt-get install python3 python3-pip virtualenvwrapper`

Create a Python3 based virtual environment.

`mkvirtualenv -p /usr/bin/python3 <venv-name>`

Set into the virtual environment.

`workon <venv-name>`

Set Project Home

`setvirtualenvproject`

Install requirements:

`pip install -r requirements`
