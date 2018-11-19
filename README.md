[![Build Status](https://travis-ci.org/giacomodeliberali/BeepBeep-MicroFlaskApp.svg?branch=master)](https://travis-ci.org/giacomodeliberali/BeepBeep-MicroFlaskApp)
[![Coverage Status](https://coveralls.io/repos/github/giacomodeliberali/BeepBeep-MicroFlaskApp/badge.svg?branch=master)](https://coveralls.io/github/giacomodeliberali/BeepBeep-MicroFlaskApp?branch=master)

BeepBeep Microservice Flask app
==================

How to run the app
-------------------

For this application to work, you need to create a Strava API application
see https://strava.github.io/api/#access and https://www.strava.com/settings/api

Once you have an application, you will have a "Client Id" and "Client Secret".
You need to export them as environment variables::

    export STRAVA_CLIENT_ID=<ID>
    export STRAVA_CLIENT_SECRET=<SECRET>

It is a good idea to create a file (and add it to .gitignore) that contains both commands. You can 
then run it via::

    source <filename>.sh

As usual, to start the app run::

    $ pip install -r requirements.txt
    $ python setup.py develop

You can then run your application with::

    $ python app.py
    * Running on http://127.0.0.1:5000/

How to create a new user
------------------------

1. Connect to Strava with the new user's account
2. Browse http://127.0.0.1:5000/create_user and insert data.
3. Login by browsing http://127.0.0.1:5000/
4. Click on "Authorize Strava Access" -- this will perform an OAuth trip to Strava.

Once authorized, you will be able to see your last 10 runs.
But for this, we need to ask the Celery worker to fetch them.
