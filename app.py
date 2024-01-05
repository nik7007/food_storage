from logging.config import dictConfig

from flask import Flask

from core import ActionTypeConverter
from food import food_route

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
logger = app.logger
app.url_map.converters.update(action_type=ActionTypeConverter)

app.register_blueprint(food_route, url_prefix='/food')


@app.route('/')
def hello_world():  # put application's code here
    logger.info("Hello World")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
