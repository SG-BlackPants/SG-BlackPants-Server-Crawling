from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 나중에는 크롬으로 볼 필요가 없으니, PhantomJS로 변경할 것
# driver = webdriver.PhantomJS('C:/Users/user/Desktop/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs')
# driver = webdriver.Chrome('C:/Users/user/Desktop/chromedriver/chromedriver')


def get_everytime_all_data(userid, password, boardnum, start_page, end_page):
    driver = webdriver.Chrome('C:/Users/user/Desktop/chromedriver/chromedriver')
    login_in_everytime(userid, password, driver)

    articles = []

    start_page = int(start_page)
    end_page = int(end_page)

    if start_page < 1:
        start_page = 1

    all_num = 0

    for i in range(start_page, end_page + 1):
        board_url = 'http://everytime.kr/'+boardnum+'/p'+'/' + str(i)
        driver.get(board_url)

        url_list = get_page_url_list(driver)

        for url in url_list:
            all_num = all_num + 1
            driver.get(url)

            time.sleep(1)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            article = soup.select('div.wrap.articles > article > a')[0]
            _article = create_json_from_crawled_data(article)
            _article['boardAddr'] = url[19:]

            # 데이터 중복 체크 -> 돌리는 순간 추가되면 어쩌지?

            articles.append(_article)

    print('총 %d 개의 데이터 전달' % all_num)
    return articles


def login_in_everytime(userid, password, driver):
    driver.get('https://khu.everytime.kr/login')
    driver.find_element_by_name('userid').send_keys(userid)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()


def get_page_url_list(driver):

    time.sleep(1)

    url_list = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all = soup.select('div.wrap.articles > article')

    for article in all:
        url = 'http://everytime.kr'+article.a['href']
        url_list.append(url)

    return url_list


def create_json_from_crawled_data(article=None):
    # article이 none일 경우 처리

    _article = {}
    _article['community'] = 'everytime'
    _article['author'] = article.h3.text  # 작성자
    _article['content'] = article.p.text  # 내용
    _article['createdDate'] = article.time['title']  # 작성시간

    # 제목이 있는 게시판과 없는 게시판이 있으므로 처리
    try:
       _article['title'] = article.h2.text  # 제목
    except Exception as e:
        _article['title'] = ''  # 제목 공란

    # 첨부 이미지
    image_list = []
    for image in article.findAll("figure"):
        image_list.append(image.img['src'])

    _article['images'] = image_list

    return _article