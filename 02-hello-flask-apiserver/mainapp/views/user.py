from flask import Blueprint

blue = Blueprint('userBlue', __name__)


@blue.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    return "<h3>hi,User-Blue user : %s</h3>" % (user_id,)
