

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

class Facebook:
    def __init__(self, **kwargs):
        self.boardAddr = kwargs.get('id', '0')
        self.content = kwargs.get('message', '')
        self.images = kwargs.get('full_picture', '')
        self.createDate = kwargs.get('created_time', '')
        self.community = 'facebook' +'/' + kwargs.get('page_id', '')
        self.title = ''
        self.author = ''

    def to_json(self):
        return dict(
            community=self.community,
            boardAddr=self.boardAddr,
            content=self.content,
            images=self.images,
            createdDate=self.createDate,
            title=self.title,
            author=self.author
        )
