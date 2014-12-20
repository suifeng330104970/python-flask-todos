Todos - simple web app implemented using Flask and Sqlalchemy for Python.
Tom Slankard <tom.slankard@here.com>

Overview
--------

Todos is a toy checklist web application, it is meant to serve as an example
demonstrating the basics of using Flask and sqlalchemy together using the
Flask-SQLAlchemy extension.

This example is not meant to demonstrate REST best practices (and if you're
familiar with REST, you will probably see why).

Requirements
------------

 * Python 2.7.X
 * virtualenv
 * sqlite3

Setup in a virtual environment
------------------------------

Create a virtual environment within the todos folder and activate it:

    cd todos
    virtualenv venv
    . venv/bin/activate

Install the dependencies:

    pip install -r requirements.txt


Running tests
-------------

    nosetests --with-cover --cover-package=todos


Launch the app
----------------

    python run.py 


