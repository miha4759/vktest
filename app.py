from flask import Flask
from flask_session import Session
import redis
from classes.config import Config

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(Config.REDIS_URL)

sess = Session()
sess.init_app(app)
from classes import views

if __name__ == '__main__':
    app.run()
