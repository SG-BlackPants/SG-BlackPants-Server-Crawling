# -- coding: utf-8 --
from flask import Blueprint, Response, jsonify, request
from app.crawling import beautifulsoup_test, facebook, everytime
from app.fbconfig import univ_list
import requests

mod = Blueprint('article', __name__, url_prefix='/article')


@mod.route('/', methods=['GET'])
def article_index():
    return 'article Index'


@mod.route('/req', methods={'GET'})
def requesttest():
    url = 'http://ec2-52-23-164-26.compute-1.amazonaws.com:3000/users'
    custom_headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    req = requests.get(url, headers=custom_headers)
    print(req.text)
    return 'success'


# GraphAPI 사용 크롤링
@mod.route('/facebook/<limit>', methods=['GET'])
def crawling_from_facebook(limit):
    print('called crawling_from_facebook()')
    univ_length = len(univ_list)

    for univ_num in range(0, univ_length):
        community_list = univ_list[univ_num]['communityList']
        univ_name = univ_list[univ_num]['schoolName']

        # Facebook Crawling
        for community_num in range(0, len(community_list)):
            page_id = community_list[community_num]
            result = facebook.get_facebook_page_feed_data(page_id, univ_name, limit)
            print(':::: Facebook crawling in %s success !!! ::::' % page_id)

    return jsonify({'result': 'success'})  # 이 부분을 나중에 변경 -> API-Server로 보내기


@mod.route('/everytime', methods=['GET'])
def crawling_from_everytime():
    univ_length = len(univ_list)

    for univ_num in range(0, univ_length):
        univ_name = univ_list[univ_num]['schoolName']

        url = univ_list[univ_num]['everytimeUrl']
        id = univ_list[univ_num]['user']['id']
        pw = univ_list[univ_num]['user']['pw']
        result = everytime.get_everytime_all_data(id, pw, url, univ_name)

    return jsonify({'result': 'end'})