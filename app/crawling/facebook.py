import requests
import json

# 할 것
# 토큰 처리
# flask 인코딩 처리

app_id = " "
app_secret = " "
# access_token = app_id + "|" + app_secret
page_id = "482012061908784"
limit = 20
access_token = "EAACEdEose0cBALOzzMDbSevLgeZB9eh6e2SyrSV3C3BFEXxSrlYkTZBG8EBqxvWVTkdkks871FEsFQbONVClv0nwz19UfILFNHdwA8r8wVOqWB2qaY60ldIZCBIHATP7LddzkHkZAZCG4uZBOyZBwieiDWJ7kmvZAAG7BVhhR33xdBIbYA8foLS2pufOSt2jSUD8hySfmDx8cAZDZD"


def test_facebook_page_data(page_id):
    print('call test_facebook_page_data()')
    base = "https://graph.facebook.com/v2.11"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    resp = requests.get(url)
    return resp.json()

def test_facebook_page_feed_data(page_id):
    print('call test_facebook_page_feed_data()')
    base = "https://graph.facebook.com/v2.11"  # Graph Api 현재 버전에 맞춤
    # node = "/" + page_id + "/feed"
    node = "/" + page_id + "/feed"
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    resp = requests.get(url)
    return resp.json()


def request_until_succeed(url):
    resp = requests.get(url)
    return resp.json()


def create_url(base, node, parameters):
    url = base + node + parameters
    return url


def get_facebook_page_feed_data(page_id):
    print('call test_facebook_page_feed_data()')
    base = "https://graph.facebook.com/v2.11"
    node = "/" + page_id + "/feed"
    parameters = "/?fields=message,link,created_time,name,id&access_token=%s" % access_token
    return request_until_succeed(create_url(base, node, parameters));