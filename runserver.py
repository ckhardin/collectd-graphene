#!/usr/bin/env python
import os
from collectd_graphene.app import create_app

if __name__ == '__main__':
    _staticdir = os.path.join(os.getcwd(), "frontend", "build")
    _templatedir = os.path.join(os.getcwd(), "frontend", "build")
    app = create_app(instance_relative_config=True,
                     static_folder=_staticdir, template_folder=_templatedir)
    app.run(host='0.0.0.0')
