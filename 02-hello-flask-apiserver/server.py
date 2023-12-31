from flask import url_for

from mainapp import app
from mainapp.views import *
from mainapp.converter.custom_converter import MobileConverter


# 配置主页
@app.route("/")
def index():
    return """
    <ul>
        <li><a href="%s">用户管理</a></li>
        <li><a href="%s">银行管理</a></li>
        <li><a href="%s">银行卡管理</a></li>
    </ul>
    """ % (url_for("userBlue.user", user_id=1),
           url_for("bankBlue.find_all"),
           url_for("cardBlue.select_bank"))


if __name__ == '__main__':
    # 注册自定义converter
    app.url_map.converters['mobile'] = MobileConverter

    # 将蓝图对象注册到flask服务中，访问url时，需要/<blue.route.rule>
    app.register_blueprint(bank.blue, url_prefix="/bank")
    # 注册时可以加上url_prefix，访问url时，需要/<url_prefix>/<blue.route.rule>
    app.register_blueprint(user.blue, url_prefix="/user")
    app.register_blueprint(card.blue, url_prefix="/card")

    app.run('localhost', 8801,
            True,  # 默认是False:不开启调式模式，Ture开启调试模式
            threaded=True,  # 默认是False:单线程，Ture开启多线程
            processes=1  # 默认是1个进程。不能同时开启多线程和多进程，否则会启动报错。(threaded=True,processes=2 此时会报错)
            )
