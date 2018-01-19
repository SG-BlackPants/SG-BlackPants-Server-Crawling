from app import fbconfig, mongo
from app.model.article import Facebook
import requests

app_id = " "
app_secret = " "
# access_token = app_id + "|" + app_secret
limit = 5
access_token = fbconfig.access_token


# test
def test_facebook_page_data(page_id):
    print('call test_facebook_page_data()')
    base = "https://graph.facebook.com/v2.11"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    resp = requests.get(url)
    return resp.json()


# test
def test_facebook_page_feed_data(page_id):
    print('call test_facebook_page_feed_data()')
    base = "https://graph.facebook.com/v2.11"  # Graph Api 현재 버전에 맞춤
    # node = "/" + page_id + "/feed"
    node = "/" + page_id + "/feed"
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    resp = requests.get(url)
    return resp.json()


def request_data_to_facebook(url):
    custom_headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    req = requests.get(url, headers=custom_headers)
    return req.json()


def create_url(base, node, parameters):
    url = base + node + parameters
    return url


def get_facebook_page_feed_url(page, token):
    # parameters setting
    base = "https://graph.facebook.com/v2.11"
    fields = "/?fields=feed.limit(%d){created_time,id,message,shares,full_picture}" % limit
    url = base + page + fields + token
    return url


def get_facebook_page_feed_data(page_id):
    print('call test_facebook_page_feed_data()')
    page = "/" + page_id
    token = "&access_token=%s" % access_token
    url = get_facebook_page_feed_url(page, token)

    resp_data = request_data_to_facebook(url)

    # 예외처리
    # 1. 토큰이 만료된 경우....? 만료 되었다는 걸 아는 순간은 request를 받고난 뒤..!
    # 2. response에 feed가 없는 경우
    datalist = resp_data['feed']    # json x dictionary o

    _crawledData = []

    i = 0
    for data in datalist['data']:
        try:
            data['page_id'] = page_id  # pageid는 직접 지정
            
            _data = Facebook(**data)  # kwargs 형태로 전달
            print(_data.to_json())
            _crawledData.append(_data.to_json())
            i = i + 1
        except Exception as e:
            print(e)

    # insert_to_database(_crawledData) # DB insert 테스트 완료
    print("총 데이터 %d개" % i)

    return _crawledData


# 데이터 리스트 insert
def insert_to_database(datalist):
    print(datalist)
    collection = mongo.db.Article
    # insert!
    try:
        collection.insert(datalist)
    except Exception as e:
        print(e)
    else:
        print('data insert success!')
