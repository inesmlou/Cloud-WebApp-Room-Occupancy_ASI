# Cloud-WebApp-Room-Occupancy_ASI
This folder contains two labs of the course Internet Systems Architectures, and the final project.

The goal of the project was to develop a Cloud web application used to manage/control room occupancy.
The system can be operated by two different class of users: admins and students. Admins manage rooms by making them available for use and observe current occupancy. Students check in/out in rooms and search for friends location.

--------------------------- App Engine ---------------------------
Guestbook

Guestbook is an example application showing basic usage of Google App
Engine. Users can read & write text messages and optionally log-in with
their Google account. Messages are stored in App Engine (NoSQL)
High Replication Datastore (HRD) and retrieved using a strongly consistent
(ancestor) query.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [NDB Datastore API][3]
- [Users API][4]

## Dependencies
- [webapp2][5]
- [jinja2][6]
- [Twitter Bootstrap][7]


## E2E Test for this sample app

A Makefile is provided to deploy and run the e2e test.

To run:

     export GAE_PROJECT=your-project-id
     make

To manually run, install the requirements

    pip install -r e2e/requirements-dev.txt

Set the environment variable to point to your deployed app:

    export GUESTBOOK_URL="http://guestbook-test-dot-useful-temple-118922.appspot.com/"

Finally, run the test

    python e2e/test_e2e.py

