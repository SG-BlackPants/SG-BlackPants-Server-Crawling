
from app import celery
from app.fbconfig import univ_list
from app.crawling import facebook,everytime
import requests


@celery.task
def say_hello():
    print('hello celery!')


#TODO : Log로 변경
@celery.task
def facebook_crawling():
    print('celery task.facebook_crawling execute ::')

    univ_length = len(univ_list)

    # 학교 별로 크롤링 하게 변경
    for univ_num in range(0, univ_length):
        community_list = univ_list[univ_num]['communityList']
        univ_name = univ_list[univ_num]['schoolName']

        # Facebook Crawling
        for community_num in range(0, len(community_list)):
            page_id = community_list[community_num]
            result = facebook.get_facebook_page_feed_data(page_id, univ_name, 10)
            print(':::: Facebook crawling in %s !!! ::::' % page_id)
        
        # everytime Crawling
        url = univ_list[univ_num]['everytimeUrl']
        id = univ_list[univ_num]['user']['id']
        pw = univ_list[univ_num]['user']['pw']
        result = everytime.get_everytime_all_data(id, pw, url, univ_name)
        print(result)

        # send post data to api server : data insert success
        send_post_to_api_server(univ_name, "2018-01-28T10:05:26+0000")

    print(':::: facebook_crawling end!!! ::::')


def send_post_to_api_server(univ_name, create_date):
    print('send post to api server')
    url = 'http://ec2-52-23-164-26.compute-1.amazonaws.com:3000/firebase/new'
    param = {
        'university': univ_name,
        'createdDate': create_date
    }
    resp = requests.post(url, data=param)
    print(resp.text)

