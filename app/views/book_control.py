from flask import Blueprint, jsonify, request
from app import mongo

mod = Blueprint('book', __name__, url_prefix='/book')


@mod.route('/', methods=['GET'])
def get_all_book():
    collection = mongo.db.book
    output = []
    for result in collection.find():
        output.append(
            {
                'name': result['name'],
                'author': result['author']
            }
        )
    return jsonify({'result': output})


@mod.route('/<book>', methods=['GET'])
def get_one_book(book):
    collection = mongo.db.book
    result = collection.find_one({'name': book})
    if result:
        output = {
                    'name': result['name'],
                    'author': result['author']
        }
    else:
        output = "nono.....i don't know hahaha"
    return jsonify({'result': output})


# post 데이터 형태 예시 : {"name": "Python from flask", "author": "daaaaah46"}
@mod.route('/add', methods=['POST'])
def add_book():
    collection = mongo.db.book
    name = request.json['name']
    author = request.json['author']
    # insert!
    book_id = collection.insert(
                        {
                            'name': name,
                            'author': author
                        }
    )
    # check insert data!
    new_book = collection.find_one(
                        {
                            '_id': book_id
                        }
    )
    output = {
                'name': new_book['name'],
                'author': new_book['author']
    }
    return jsonify({'result': output})