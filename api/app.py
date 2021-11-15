from flask import Flask

from api.api_blueprint import api_bp
from api.common import ma, db


def create_app():
    flask = Flask(__name__)
    flask.register_blueprint(api_bp)
    db.init_app(flask)
    ma.init_app(flask)
    return flask


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
