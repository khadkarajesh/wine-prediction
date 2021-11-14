from flask import Flask

from api.api_blueprint import api_bp


def create_app():
    flask = Flask(__name__)
    flask.register_blueprint(api_bp)
    return flask


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
