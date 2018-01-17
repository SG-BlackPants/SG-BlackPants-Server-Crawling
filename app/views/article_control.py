# -- coding: utf-8 --
from flask import Blueprint, Response, jsonify, make_response
from app.crawling import beautifulsoup_test, facebook
import json

mod = Blueprint('article', __name__, url_prefix='/article')


@mod.route('/', methods=['GET'])
def article_index():
    return 'article Index'


@mod.route('/test', methods=['GET'])
def crawling_test():
    beautifulsoup_test.test1()
    return Response(status=200)


@mod.route('/facebook/<page_id>', methods=['GET'])
def crawling_from_facebook(page_id):
    crawled_data = facebook.get_facebook_page_feed_data(page_id)
    return jsonify({'result': crawled_data})

