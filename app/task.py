from app import celery
from app.fbconfig import community_list
from app.crawling import facebook


@celery.task
def say_hello():
    print('hello celery!')


@celery.task
def facebook_crawling(univ_name, number):
    print('called crawling_from_facebook()')

    # # 페이지 번호가 잘못 들어올 경우가 있을까?
    _number = int(number)

    # if (_number < 0 or
    #         _number >= len(community_list[univ_name])):
    #     print('number에 문제가 있군요')
    #     return jsonify({'result': "잘못된 요청 또는 URL을 전달하였습니다"})  # 500에러도 보내야할까?
    # else:
    page_id = community_list[univ_name][_number]['id']
    result = facebook.get_facebook_page_feed_data(page_id, univ_name)
    print('result is %s' % result)