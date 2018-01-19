# -- coding: utf-8 --
from flask import Blueprint, Response, jsonify, make_response
from app.crawling import beautifulsoup_test, facebook
from app.fbconfig import community_list

mod = Blueprint('article', __name__, url_prefix='/article')


@mod.route('/', methods=['GET'])
def article_index():
    return 'article Index'


@mod.route('/test', methods=['GET'])
def crawling_test():
    beautifulsoup_test.test1()
    return Response(status=200)


# page_id를 받는 게 아니고, kyunghee/1 이런 식으로 받자
@mod.route('/facebook/<univ_name>/<number>', methods=['GET'])
def crawling_from_facebook(univ_name, number):
    print('called crawling_from_facebook()')

    # 페이지 번호가 잘못 들어올 경우가 있을까?
    _number = int(number)

    if(_number < 0 or
            _number >= len(community_list[univ_name])):
        print('number에 문제가 있군요')
        return jsonify({'result': "잘못된 요청 또는 URL을 전달하였습니다"})   # 500에러도 보내야할까?
    else:
        page_id = community_list[univ_name][_number]['id']
        crawled_data = facebook.get_facebook_page_feed_data(page_id)
        return jsonify({'result': crawled_data})
