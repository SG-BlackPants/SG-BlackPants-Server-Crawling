from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)


from app.views import general               # general은 기본 라우팅 용
app.register_blueprint(general.mod)
from app.views import book_control          # Book은 테스트 용 입니다요
app.register_blueprint(book_control.mod)
from app.views import article_control
app.register_blueprint(article_control.mod)
