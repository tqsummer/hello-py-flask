from flask import Blueprint

blue = Blueprint('userBlue', __name__)


@blue.route('/user', methods=['GET', 'POST'])
def user():
    return "<h3>hi,User-Blue</h3>"
