# How to install

- Install this as a Python project
 - remember to install dependencies listed in requirements.txt also!
- Put in cron 'python manage.py scrape' each 12 hours (or each hour, as you need)

# Endpoints to use

You should use a GET method on /rates/ endpoint. There is an optional parameter called
_date_ which can be used to specify a particular date to query in format of YYYY-MM-DD.
The default value is today, which will be frequently unavailable.

# The architecture

The architecture consists of a WSGI REST interface, supplied by Django.
It also consists of a command, meant to be put inside cron, of
`python3 manage.py scrape`. This command must be ran inside the directory.

You can also switch to another database in [settings.py](sunscrapers/settings.py).

