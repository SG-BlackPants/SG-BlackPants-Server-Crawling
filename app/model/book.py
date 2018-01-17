# 이건 그냥 테스트용
class Book:
    name = ""
    author = ""

    # 파이썬의 기본 생성자
    def __init__(self): 
        pass

    # 편의상 클래스와 같은 이름의 함수를 만들었음
    def Book(self, name, author):
        self.name = name
        self.author = author

    # 클래스의 내용을 JSON으로 보냄, DB 테스트용
    def convert_insert_form(self):
        rv = (
                {
                    "name": self.name,
                    "author": self.author
                }
            )
        return rv