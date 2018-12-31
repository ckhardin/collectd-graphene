Flask+Graphene+RRD Project
==========================

This project shows a simple integration between Graphene, Flask, and
a Collectd RRD datasets. The goal is to show a python only implementation
of serving the RRD dataset to a Client side renderer based on d3.js.

In reviewing other collectd front ends, it appearred that they relied on
a perl runtime to generate images and so the main objective for this
implementation is to only user python on the server side and a javascript
client visualization.


Getting Started
---

The sources of the project are organized as a flask application and
run under [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs).
Unfortunately, the python-rrdtool package from the pip needs to be
compiled which is not always possible on all systems. So, the virtualenv
is setup to allow the system site packages, which is not the default

```bash
cd collectd-graphene
virtualenv --system-site-packages env
source env/bin/activate
```

And now install the requirements/dependencies in the virtualenv

```bash
pip install -r requirements.txt
```

Start the server and run the application

```bash
python ./runserver.py
```

This would provide a service on the localhost at
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) to
access and run the basic queries.

