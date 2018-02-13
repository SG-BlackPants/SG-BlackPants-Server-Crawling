# -*- coding: utf-8 -*-
from app import fbconfig
from dateutil import parser
from app.model.article import Article
import requests

# access_token = app_id + "|" + app_secret
limit = 300
access_token = fbconfig.access_token


def request_data_to_facebook(url):
    custom_headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    req = requests.get(url, headers=custom_headers)
    return req.json()


def get_facebook_page_info_url(page_id):
    base = "https://graph.facebook.com/v2.11"
    node_id = "/" + page_id
    fields = "?fields=id,name"
    token = "&access_token=%s" % access_token
    url = base + node_id + fields + token
    return url



def get_facebook_page_feed_url(page, token):
    # parameters setting
    base = "https://graph.facebook.com/v2.11"
    fields = "/?fields=feed.limit(%d){created_time,id,message,shares,full_picture}" % limit
    url = base + page + fields + token
    return url


def get_feed_images_url(content_id):
    base = "https://graph.facebook.com/v2.11"
    feed_id = "/" + content_id
    fields = "/?fields=attachments"
    token = "&access_token=%s" % access_token
    url = base + feed_id + fields + token
    return url


def get_facebook_page_feed_data(page_id, univ_name):
    print('call test_facebook_page_feed_data()')

    page = "/" + page_id
    token = "&access_token=%s" % access_token
    url = get_facebook_page_feed_url(page, token)

    resp_data = request_data_to_facebook(url)

    # 비교 객체 생성
    article = Article()

    lately_date = article.get_community_lately_data(univ_name, 'facebook', page_id)

    i = 0
    _crawledData = []

    # 예외처리
    try:
        data_list = resp_data['feed']    # Dict
        for data in data_list['data']:
            try:
                created_time = set_date_format_to_datetime(data['created_time'])

                # 만약에 data 가 lately_date 보다 빠르다면? : 새롭게 저장할 데이터
                if compare_date_with_lately_date(lately_date, created_time) is True:
                    _data = create_json_from_crawled_data(data, page_id, univ_name)
                    _crawledData.append(_data)
                    i = i + 1

                # 만약에 date 가 lately_date 보다 느리다면? : 이미 이전에 크롤링 한 데이터임
                else:
                    pass

            except Exception as e:
                print('\n get_facebook_page_feed_data error() in for :::: ', e)

    except Exception as e:
        # 토큰이 만료된 경우 에러 (만료 되었다는 걸 아는 순간은 request 를 받고난 뒤..!)
        # response 에 feed 가 없는 경우
        print('\n get_facebook_page_feed_data error() :::: ' + e)

    # 데이터베이스에 insert
    article.insert_to_database(_crawledData)

    # 데이터 갯수 Check
    print("count of Data : %d" % i)

    return 'success'


def set_date_format_to_datetime(create_date=None):
    print(create_date)
    if create_date is None:
        return None

    else:
        try:
            date = parser.parse(create_date)
            return date

        except Exception as e:
            print('\n set_date_format_to_datetime() :::: ' + e)
            return None


def get_feed_image_data_list(content_id):
    image_list = []
    url = get_feed_images_url(content_id)
    resp_data = request_data_to_facebook(url)

    # subattachment 있는 경우 -> 사진 여러개
    # subattachment 없고, media가 있는 경우 -> 사진 한 개
    # subattachment도 없고, media도 없는 경우 -> 사진 없음
    try:
        if 'attachments' in resp_data:
            data = resp_data['attachments']['data'][0]

            if 'subattachments' in data:
                # print('\n multiple images')
                media_list = data['subattachments']['data']

                for media in media_list:
                    image = media['media']['image']
                    src = image['src']
                    image_list.append(src)

            elif 'media' in data:
                # print('\n single images')
                image = data['media']['image']
                src = image['src']
                image_list.append(src)

        else:
            # print('\n image is none')
            pass

    except Exception as e:
        # 토큰이 만료된 경우 에러 (만료 되었다는 걸 아는 순간은 request를 받고난 뒤..!)
        # response에 feed가 없는 경우
        print('\n get_feed_image_data_list() error :::: ', e)
    return image_list


def get_facebook_page_info_data(page_id):
    url = get_facebook_page_info_url(page_id)
    resp_data = request_data_to_facebook(url)

    data = ''

    try:
        data = resp_data["name"]
    except Exception as e:
        print('\n get_facebook_page_info_data() error :::: ', e)
    return data


def create_json_from_crawled_data(article=None, page_id='', univ_name=''):
    # article이 none일 경우 처리

    if article is None:
        pass

    community_name = get_facebook_page_info_data(page_id)

    _article = {}
    _article['community'] = 'facebook'+'/'+ community_name
    _article['boardAddr'] = article['id']
    _article['university'] = univ_name
    _article['author'] = community_name
    _article['content'] = article['message']
    _article['createdDate'] = set_date_format_to_datetime(article['created_time'])
    _article['title'] = ''  # 제목 공란

    # 첨부 이미지
    image_list = get_feed_image_data_list(article['id'])
    _article['images'] = image_list

    return _article


def compare_date_with_lately_date(standard_date, compare_date):
    # 새로운 데이터일 경우, True, 새로운 데이터가 아닐 경우 False
    return True if standard_date < compare_date else False
