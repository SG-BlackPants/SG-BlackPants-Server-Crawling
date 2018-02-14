# -*- coding: utf-8 -*-
from flask import Flask
from flask_pymongo import PyMongo
from celery.schedules import crontab
from datetime import timedelta
from app import celeryconfig

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)

app.config.update(
    CELERY_BROKER_URL='amqp://guest:guest@localhost:5672/',
    CELERY_RESULT_BACKEND='amqp://',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    # CELERY_ROUTES={'app.task.facebook_crawling': {'queue': 'feeds'}},
    CELERYBEAT_SCHEDULE={
        'facebook_crawling': {
            'task': 'app.task.facebook_crawling',
            # 'schedule': crontab(hour='*', minute='5'),
            'schedule': timedelta(seconds=180),
            'args': ()
        }
    }
)

celery = celeryconfig.make_celery(app)


from app.views import general               # general은 기본 라우팅 용
app.register_blueprint(general.mod)
from app.views import book_control          # Book은 테스트 용 입니다요
app.register_blueprint(book_control.mod)
from app.views import article_control
app.register_blueprint(article_control.mod)
