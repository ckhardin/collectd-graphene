import os

from flask import Flask, render_template
from flask_graphql import GraphQLView

from .schema import schema


def create_app(**kwargs):
    # Adjust flask to service a "built" frontend
    app = Flask(__name__, **kwargs)
    app.config.from_object('flaskrrd.config')

    # create instance directory
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.add_url_rule('/graphql',
                     view_func=GraphQLView.as_view('graphql',
                                                   schema=schema, graphiql=True))

    @app.route('/', methods=['GET'])
    def root():
        return render_template('index.html')

    @app.route('/<path:path>')
    def static_file(path):
        return app.send_static_file(path)

    return app
