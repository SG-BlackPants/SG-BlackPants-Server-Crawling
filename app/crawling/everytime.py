# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from app.model.article import Article
import time
import config
import pytz
import datetime

# 나중에는 크롬으로 볼 필요가 없으니, PhantomJS로 변경할 것
# driver = webdriver.PhantomJS('./phantomjs')
# driver = webdriver.Chrome('./chromedriver')


def get_everytime_all_data(userid, password, everytime_url, univ_name):
    driver = webdriver.PhantomJS(config.Chrome_driver_path)
    login_in_everytime(userid, password, driver)

    # TODO : 이렇게 안하게 수정
    start_page = 1
    end_page = 1

    if start_page < 1:
        start_page = 1

    num = 0  # insert 데이터 갯수 측정
    a = Article()
    lately_date = a.get_community_lately_data(univ_name, 'everytime')

    url_list = get_board_urls(driver, everytime_url)

    for url in url_list:
        for i in range(start_page, end_page + 1):
            url = url + '/p/' + str(i)
            driver.get(url)

            # 해당 게시판 내 페이지(board_url)에 있는 게시글 url을 모두 가져옴
            article_url_list = get_page_url_list(driver)

            # url 의 갯수 (20개) 만큼 for 문을 돌린다.
            for article_url in article_url_list:
                driver.get(article_url)
                time.sleep(1)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    article = soup.select('div.wrap.articles > article > a')[0]

                    # 해당 게시글의 날짜 및 시간을 가져옴
                    article_time = set_date_format_to_datetime(article.time['title'])

                    # 해당 게시글의 날짜 및 시간이 기존 데이터보다 이후인 경우 수행한다.
                    if compare_date_with_lately_date(lately_date, article_time) is True:

                        # 데이터 구조화
                        _data = create_json_from_crawled_data(article, article_time)
                        _data['university'] = univ_name
                        _data['boardAddr'] = article_url[19:]

                        a.insert_to_database(_data)
                        num = num + 1  # insert 의 개수 + 1

                    # 해당 게시글의 날짜 및 시간이 기존 데이터보다 이전인 경우
                    # 더이상 크롤링을 수행하지 않아도 되기 때문에 for 문을 빠져나간다.
                    else:
                        break

                except Exception as e:
                    print('get_everytime_all_data() in for :::: ', e)

    print("count of Data : %d" % num)

    return dict(
        result='success',
        count=num,
        lately_date=lately_date
    )


def get_board_urls(driver, url):
    driver.get(url)
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    group = soup.findAll('div', {'class': 'group'})
    board_url = list()

    for i in range(0, 2):  # for(int i=0; i<2; i++)
        li = group[i].findAll('a', {'class': 'new'})
        for a in li:
            url = 'http://everytime.kr' + a['href']
            board_url.append(url)

    return board_url


def login_in_everytime(userid, password, driver):
    driver.get('https://everytime.kr/login')
    driver.find_element_by_name('userid').send_keys(userid)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()


def get_page_url_list(driver):

    time.sleep(1)

    url_list = list()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    alldata = soup.select('div.wrap.articles > article')

    for article in alldata:
        url = 'http://everytime.kr'+article.a['href']
        url_list.append(url)

    return url_list


def create_json_from_crawled_data(article=None, article_time=''):
    # article이 none일 경우 처리

    _article = dict()
    _article['community'] = 'everytime'
    _article['author'] = article.h3.text  # 작성자
    _article['content'] = article.p.text  # 내용
    _article['createdDate'] = article_time  # 작성시간

    # 제목이 있는 게시판과 없는 게시판이 있으므로 처리
    try:
       _article['title'] = article.h2.text  # 제목
    except Exception as e:
        _article['title'] = ''  # 제목을 공란으로 처리

    # 첨부 이미지
    image_list = []
    for image in article.findAll("figure"):
        image_list.append(image.img['src'])

    _article['images'] = image_list

    return _article


def set_date_format_to_datetime(create_date=None):
    if create_date is None:
        return None

    else:
        try:
            date = datetime.datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
            date = date.replace(tzinfo=pytz.UTC)
            return date

        except Exception as e:
            print('\n set_date_format_to_datetime() :::: ' + e)
            return None


# standard_date : 기준 날짜 (lately_date)
# compare_date  : 비교 날짜
# TODO : 삼항연산자로 변경
def compare_date_with_lately_date(standard_date, compare_date):
    # 새로운 데이터일 경우, True, 새로운 데이터가 아닐 경우 False
    rv = True if standard_date < compare_date else False
    return rv
