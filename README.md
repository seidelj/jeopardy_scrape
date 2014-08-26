jeopardy_scrape
===============

Scrapes the j-archive using a the django framework.  While it imposes a decent ammount of overhead, Django's ORM is very nice to work with.

You'll need to have knowledge of setting up a django project.
https://www.djangoproject.com/

### There is no need to runserver.  The project can be run using the following. ###

      $(venv) python download.py
      $(venv) python parse.py


I added earnings and contestants however credit is due to: https://github.com/whymarrh/jeopardy-parser
