import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'test.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #register db
    from . import db
    db.init_app(app)

    #register blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    #register bbs
    from . import bbs
    app.register_blueprint(bbs.bp)
    app.add_url_rule('/', endpoint='index')

    # register profile 
    from . import profile
    app.register_blueprint(profile.bp)

    #register post
    from . import post
    app.register_blueprint(post.bp)

    return app