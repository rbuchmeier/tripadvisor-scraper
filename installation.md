https://stackoverflow.com/questions/23842713/using-python-3-in-virtualenv

# Installing on a Mac:

`xcode-select --install`

Install Brew:

`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

`brew install python`

`brew cask install chromedriver`

`pip3 install virtualenvwrapper`

`touch .bash_profile`

`echo "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3" >> .bash_profile`

`echo "source /usr/bin/virtualenvwrapper.sh" >> .bash_profile`

`source .bash_profile`

Install Project from Github:

`git clone https://github.com/mariomarine/tripadvisor-scraper/; cd tripadvisor-scraper`

Create a Python3 based virtual environment.

`mkvirtualenv -p /usr/bin/python3 tripadvisor-scraper`

Set into the virtual environment.

`workon tripadvisor-scraper`

Set Project Home

`setvirtualenvproject`

Install requirements:

`pip install -r requirements`
