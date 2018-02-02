from app import fbconfig, mongo
import requests

# access_token = app_id + "|" + app_secret
limit = 10
access_token = fbconfig.access_token

def request_data_to_facebook(url):
    custom_headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    req = requests.get(url, headers=custom_headers)
    return req.json()


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
                _data = create_json_from_crawled_data(data, page_id)
                # print(_data.to_json())
                _crawledData.append(_data)
                i = i + 1
            except Exception as e:
                print('\n get_facebook_page_feed_data error() in for :::: ', e)

    except Exception as e:
        # 토큰이 만료된 경우 에러 (만료 되었다는 걸 아는 순간은 request를 받고난 뒤..!)
        # response에 feed가 없는 경우
        print('\n get_facebook_page_feed_data error() :::: ' + e)
    
    insert_to_database(_crawledData)  # DB insert 테스트 완료
    print("count of Data : %d" % i)

    return _crawledData


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


def create_json_from_crawled_data(article=None, page_id=''):
    # article이 none일 경우 처리

    _article = {}
    _article['community'] = 'facebook'+'/'+ page_id
    _article['boardAddr'] = article['id']
    _article['author'] = page_id
    _article['content'] = article['message']
    _article['createdDate'] = article['created_time']
    _article['title'] = ''  # 제목 공란

    # 첨부 이미지
    image_list = get_feed_image_data_list(article['id'])
    _article['images'] = image_list

    return _article


# 데이터 리스트 insert
def insert_to_database(datalist):
    # print(datalist)
    collection = mongo.db.Article
    # insert!
    try:
        collection.insert(datalist)
    except Exception as e:
        print(e)
    else:
        print('data insert success!')
