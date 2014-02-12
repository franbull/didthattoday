didthattoday README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_didthattoday_db development.ini

- $VENV/bin/pserve development.ini

***********************

- some dependencies are listed in requirements.pip and not in setup.py so do:
- $ pip install -r requirements.pip

- run the tests with::
- $ py.test
- it will run all files starting with test_ and find test methods in there that
  start with test_
