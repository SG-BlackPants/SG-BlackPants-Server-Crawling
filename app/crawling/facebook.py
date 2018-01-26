from bs4 import BeautifulSoup
from selenium import webdriver
import time
import config

def get_facebook_page_all_data(email, password, url):
    driver = webdriver.Chrome(config.Chrome_driver_path)
    driver.get('https://www.facebook.com/')
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('pass').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,2500)") # 나중에 숫자 말고 화면 높이로 변경 ㄱ
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,2500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,2500)")
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all = soup.find_all('div', {'class': '_1dwg _1w_m _q7o'})

    for feed in all:
        contents = feed.find_all('', {'class': '_5pbx userContent'})

        if not contents:  # contents = []
            pass
        else:
            content = contents[0]
            print(content.p)

        imageurl_list = []

        imagediv = feed.find_all('a', {'class': '_5dec _xcx'})

        for image in imagediv:
            imageurl = image['data-ploi']
            imageurl_list.append(imageurl)
        print(imageurl_list)

    articles = []
    return articles



# 버려야 할 듯..? ㅠㅠ
from app import fbconfig, mongo
from app.model.article import Facebook
import requests

app_id = " "
app_secret = " "
# access_token = app_id + "|" + app_secret
limit = 5
access_token = fbconfig.access_token


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

    i = 0
    _crawledData = []

    # 예외처리
    try:
        datalist = resp_data['feed']    # json x dictionary o
        for data in datalist['data']:
            try:
                data['page_id'] = page_id  # pageid는 직접 지정
                _data = Facebook(**data)  # kwargs 형태로 전달
                # print(_data.to_json())
                _crawledData.append(_data.to_dict())
                i = i + 1
            except Exception as e:
                print(e)

    except Exception as e:
        # 토큰이 만료된 경우 에러 (만료 되었다는 걸 아는 순간은 request를 받고난 뒤..!)
        # response에 feed가 없는 경우
        print(e)
    
    # insert_to_database(_crawledData) # DB insert 테스트 완료
    print("count of Data : %d" % i)

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
