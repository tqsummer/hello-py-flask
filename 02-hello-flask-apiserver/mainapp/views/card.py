from flask import Blueprint, url_for

blue = Blueprint('cardBlue', __name__)


@blue.route('/add/<bank_name>')
def add_card(bank_name):
    return "%s 开户成功！" % (bank_name)


@blue.route('select_bank')
def select_bank():
    bank_name = "招商银行"
    return """
    选择银行成功，3秒后<a href ="%s">进入开户页</a>
    """ % (url_for("cardBlue.add_card", bank_name=bank_name))
