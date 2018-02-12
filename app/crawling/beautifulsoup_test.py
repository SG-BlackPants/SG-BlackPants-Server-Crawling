import requests
from bs4 import BeautifulSoup


html = '''<!DOCTYPE html>
<html>
<head><title>The Dormouse's story</title></head>
<body>
    <p class="title">
        <b>The Dormouse's story</b>
    </p>
    <p class="story">
        Once upon a time there were three little sisters; and their names were
        <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
        <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
        <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
        and they lived at the bottom of a well.
    </p>
</body>
</html>
'''


def test1():
    print('call test() in beautifulsoup_test.py')

    soup = BeautifulSoup(html, 'html.parser')

    print('#### element ####')
    print(soup.title)                           # <title>The Dormouse's story</title>

    print('#### tag ####')
    print(soup.title.name)                      # title

    print('#### text ####')
    print(soup.title.string)                    # The Dormouse's story
    print(soup.title.get_text())                # The Dormouse's story

    print('#### p ####')
    print(soup.p)

    print('#### single element ####')
    print(soup.a.get_text())                    # Elsie

    print('#### multi element ####')
    print(soup.find_all('a'))                   # [
                                                # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
                                                # <a class="sister" href="http://example.com/Lacie" id="link2">Lacie</a>,
                                                # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
                                                # ]

    print(soup.find_all('a')[0].get_text())     # Elsie
    print(soup.find_all('a')[1].get_text())     # Lacie

    print('#### attribute ####')
    print(soup.a['class'])                      # ['sister']
    print(soup.a.get('class'))                  # ['sister']
    print(soup.a['href'])                       # http://example.com/elsie
    print(soup.a.attrs['href'])                 # http://example.com/elsie

    print('#### find by id ####')
    print(soup.find(id='link1'))                # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
    print(soup.find('', {'id':'link1'}))        # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

    print('#### find by class ####')
    print(soup.find_all(class_='sister'))
    print(soup.find_all('', {'class':'sister'}))    # [
                                                    # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
                                                    # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
                                                    # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
                                                    # ]