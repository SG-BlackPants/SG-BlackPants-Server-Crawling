from bs4 import BeautifulSoup
from selenium import webdriver

# 나중에는 크롬으로 볼 필요가 없으니, PhantomJS로 변경할 것
# driver = webdriver.PhantomJS('C:/Users/user/Desktop/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs')


def test_naver_pay_data(id, pw):
    driver = webdriver.Chrome('C:/Users/user/Desktop/chromedriver/chromedriver')

    driver.get('https://nid.naver.com/nidlogin.login')
    driver.find_element_by_id('id').send_keys(id)
    driver.find_element_by_id('pw').send_keys(pw)

    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/span[2]/a').click()

    driver.get('https://order.pay.naver.com/home')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    notices = soup.select('div.p_inr > div.p_info > a > span')
    return notices


def get_everytime_data(id, pw):
    driver = webdriver.Chrome('C:/Users/user/Desktop/chromedriver/chromedriver')
    driver.get('https://khu.everytime.kr/login')
    driver.find_element_by_id('userid').send_keys(id)
    driver.find_element_by_id('password').send_keys(pw)
    return 'success!'
