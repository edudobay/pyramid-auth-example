==============================
Pyramid authentication example
==============================

This is an example of how an authentication token can be passed to a Pyramid
application via a query string parameter and handled globally. Advanced parsing
of the token is outside the scope, thus I implemented only a “dumb token” that
simply contains the username in cleartext.

Setup
-----

When in the root directory of this repo:

* Create a virtual environment, if desired (I did: ``virtualenv -p python3 .venv``; then ``source .venv/bin/activate``)
* ``python setup.py develop``
* Ready to ride!

Running the application
-----------------------

Each of the following illustrates one of two methods of implementing the said feature::

 pserve development.ini authmode=policy
 pserve development.ini authmode=redirect

Notes
-----

In either case, the main point is using a query string to log in, as in::

 http://localhost:6543/info?token=joe
 --> will log in as user `joe`


Authentication via request handler and redirect
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Seems like the shortest code: a request handler checks for the ``token`` GET parameter and, having found it, pops it and emits a redirect to the same URL with that parameter removed, also saving the login cookie. But an additional request is made.


Authentication via custom policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To avoid this extra request, I ended up subclassing the default ``AuthTktAuthenticationPolicy`` and adding extra functionality that checks for the ``token`` GET parameter. In this check I add a callback that will add to the response the headers for saving the login cookie. I needed to save the username to a new field (i.e. added by me) in the Request object — which I think wasn’t quite the nicest idea — to avoid adding the callback repeatedly every time; instead the ``token`` is popped from GET the first time it is read.

