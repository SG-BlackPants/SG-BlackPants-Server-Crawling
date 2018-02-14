# -*- coding: utf-8 -*-
from app import mongo
import datetime
import pytz

"""
    _id             : ObjectID
    community       : String
    board_address   : String
    title           : String
    author          : String
    content         : String
    images          : Array
    createdDate     : Date
"""


class Article:
    def __init__(self, **kwargs):
        # self.boardAddr = kwargs.get('id', '0')
        # self.content = kwargs.get('message', '')
        # self.images = kwargs.get('full_picture', '')
        # self.createDate = kwargs.get('created_time', '')
        # self.community = 'facebook' +'/' + kwargs.get('page_id', '')
        # self.title = ''
        # self.author = ''
        self.collection = mongo.db.articles

    def to_dict(self):
        return dict(
            community=self.community,
            boardAddr=self.boardAddr,
            content=self.content,
            images=self.images,
            createdDate=self.createDate,
            title=self.title,
            author=self.author
        )

    # 데이터 중, 해당 커뮤니티에서 가장 최신 글을 불러옴
    def get_community_lately_data(self, university=None, community=None, page_id=''):

        # community 가 없는 경우, 데이터베이스에서 추적 불가능
        if community is None or university is None:
            return None

        else:

            date = None

            # facebook 의 경우, facebook/{커뮤니티 아이디} 로 학교에 해당하는 커뮤니티 구분
            # everytime 의 경우, everytime 하나로 고정
            if community is 'facebook':
                community_id = '-' + page_id
            elif community is 'everytime':
                community_id = ''

            print(community_id)

            try:
                cursor = self.collection \
                        .find({'university': university, 'community': community + community_id}) \
                        .sort([('createdDate', -1)]) \
                        .limit(1)

                lately_data = cursor[0]
                date = lately_data["createdDate"]  # 'datetime.datetime' 타입

            except Exception as e:
                print(e)

            # MongoDB 에 이미 값들이 들어있기 때문에 초기값을 받아올 때 외에는 사용하지 않음
            # but, 새로운 학교나 커뮤니티가 추가될 시에는 datetime_str을 수정하여 어느 시점의 데이터부터 가져올 건지 설정
            if date is None:
                datetime_str = '2018-01-01 00:00:00'
                date = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

            date = date.replace(tzinfo=pytz.UTC)
            print('lately_date timeZone :: \n', date.tzinfo)
            print('lately_date :: ', date)
            return date

    # 데이터 리스트 insert
    def insert_to_database(self, data_list):
        # print(data_list)
        # insert!
        try:
            self.collection.insert(data_list)
        except Exception as e:
            print(e)
        else:
            print('data insert success!')