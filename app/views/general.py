from flask import Blueprint


mod = Blueprint('general', __name__)


@mod.route('/')
def index():
    return 'index Page'


@mod.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

