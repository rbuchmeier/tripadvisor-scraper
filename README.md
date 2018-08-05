# tripadvisor-scraper

*Please give credit to Ferdinand Mütsch for creating the following gist:*
https://gist.github.com/n1try/be52a86b82bbb1aa9c357125028eb7ca

## Installation

Install or download the repo:

`git clone https://github.com/mariomarine/tripadvisor-scraper/`

Install requirements (recommendation: use a virtualenv with python3):

`pip install -r requirements`

Run file:

`python tripadvisor_scraper.py -e chrome -o reviews.csv https://www.tripadvisor.com/Restaurant_Review-g60502-d804358-Reviews-Cowfish-Lander_Wyoming.html`

## Advice

Please be conscious whenever you scrape any website. Leave plenty of time between requests.
If we overload their server it will ruin the data-collection for everyone.
