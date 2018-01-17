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
    def __init__(self, community, board_address, title, author, content, images, createdDate):
        self.community = community
        self.board_address = board_address
        self.title = title
        self.author = author
        self.content = content
        self.images = images
        self.createDate = createdDate

    @property
    def community(self):
        return self.community

    @community.setter
    def community(self, community):
        self.community = community


