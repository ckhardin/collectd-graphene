Flask+Graphene+RRD Project
==========================

This project shows a simple integration between Graphene, Flask, and
a Collectd RRD datasets. The goal is to show a python only implementation
of serving the RRD dataset to a Client side renderer based on d3.js.

In reviewing other collectd front ends, it appearred that they relied on
a perl runtime to generate images and so the main objective for this
implementation is to only user python on the server side and a javascript
client visualization.
