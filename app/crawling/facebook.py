from app import fbconfig
import requests

app_id = " "
app_secret = " "
# access_token = app_id + "|" + app_secret
limit = 20
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


def get_facebook_page_feed_url(base, page, token):
    # parameters setting
    fields = "/?fields=feed.limit(%d){created_time,id,message,shares,full_picture}" % limit
    url = base + page + fields + token
    return url


def get_facebook_page_feed_data(page_id):
    print('call test_facebook_page_feed_data()')
    base = "https://graph.facebook.com/v2.11"
    page = "/" + page_id
    token = "&access_token=%s" % access_token
    url = get_facebook_page_feed_url(base, page, token)

    resp_data = request_data_to_facebook(url)
    print(resp_data)

    # 예외처리
    # 1. 토큰이 만료된 경우
    # 2. response에 feed가 없는 경우
    datalist = resp_data['feed']    # json x dictionary o

    _crawledData = []

    i = 0
    for data in datalist['data']:
        # 데이터 예외처리
        _data = {
            'community': '',
            'boardAddr': data['id'],
            'title': '',
            'author': '',
            'content': data['message'],
            'images': data['full_picture'],
            'createdDate': data['created_time']
        }
        _crawledData.append(_data)
        i = i + 1

    print("총 데이터 %d개" % i)

    return _crawledData
