from flask import Blueprint
from flask import request, jsonify, redirect, url_for
from mainapp.dao import bank_dao

# 创建蓝图时
# 第一个参数：name可以任意命名
# 第二个参数：必须使用__name__表示模块名
blue = Blueprint('bankBlue', __name__)


def type_str(v_type):
    if v_type:
        return str(type(v_type)).replace("<", "").replace(">", "")


@blue.route('/find_all', methods=['GET', 'POST'])
def find_all():
    dao = bank_dao.BankDao()
    result = dao.find_all()
    return jsonify(result)


'''
路由参数转换器
converter : string (default), int , float , path
'''


@blue.route('/find_keyword/<keyword>', methods=['GET'])
def find_keyword(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_string/<string:keyword>', methods=['GET'])
def find_string(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_string_kwargs/<string(minlength=3,maxlength=8):keyword>', methods=['GET'])
def find_string_kwargs(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_int/<int:keyword>', methods=['GET'])
def find_int(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_float/<float:keyword>', methods=['GET'])
def find_float(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_path/<path:keyword>', methods=['GET'])
def find_path(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_mobile/<mobile:keyword>', methods=['GET'])
def find_mobile(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


@blue.route('/find_mobile_redirect/<redirect_keyword>', methods=['GET'])
def find_mobile_redirect(redirect_keyword):
    # url_for来触发mobile参数转换器to_url函数调用
    # 使用蓝图时,endpoint格式是：模块蓝图名.endpoint名
    redirect_url = url_for("bankBlue.find_mobile", keyword=redirect_keyword)
    # 重定义到指定url
    return redirect(redirect_url)


# 匹配任意any()中的字符串
# a.b
# ab
# cd
# int # 这个是int字符串，不是int类型的值
# str # 这个是str字符串，不是str类型的值
# ab,bc
@blue.route('/find_any/<any(a.b,ab,cd,int,str,"ab,bc"):keyword>', methods=['GET'])
def find_any(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)


'''

'''


@blue.route('/delete', methods=['GET', 'POST'])
def delete():
    bank_id = request.args.get("id")
    return "<h3>Delete Bank-Blue : %s</h3> " % (bank_id,)


@blue.route('/edit/<int:bank_id>', methods=['GET'])
def edit(bank_id):
    return "editing : %s" % (bank_id,)
