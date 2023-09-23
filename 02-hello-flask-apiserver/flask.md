# Flask

## Flask-Script插件

Flask app托管给flask-script的Manager进行管理，可以过命令行方式进行启动Flask服务

* 注： Flask==2.3.3 Flask-Script==2.0.6 这两个版本会有冲突，无法使用Manager进行管理Flask app

```shell
# 安装flask-script
pip install flask-script
```

```python
# mainapp包__init__.py
from flask import Flask

app = Flask(__name__)

```

```python
# server.py
from mainapp import app
from flask_script import Manager

if __name__ == '__main__':
    manager = Manager(app)
    manager.run()
```

```shell
# 启动flask服务(跟启动django方式类似)    
python server.py runserver
```

## Flask-Blueprint插件

插件功能：主要是拆分view模块，将相同功能模块分到一个view脚本中。

```shell
# 安装flask-blueprint
pip install flask-blueprint
```

```python
# bank_dao.py
from flask import Blueprint

# 创建蓝图对象，每个模块需要定义一个蓝图对象，需要注册到app中
# 第一个参数：name可以任意命名
# 第二个参数：必须使用__name__表示模块名
blue = Blueprint('bankBlue', __name__)


@blue.route('/bank', methods=['GET', 'POST'])
def bank():
    return "<h3>hi,Bank-Blue</h3>"
```

```python
# server.py
from mainapp import app
# 引用蓝图模块
from mainapp.views import *

if __name__ == '__main__':
    # 将蓝图对象注册到flask服务中，访问url时，需要/<blue.route.rule>
    app.register_blueprint(bank.blue)
    # 注册时可以加上url_prefix，访问url时，需要/<url_prefix>/<blue.route.rule>
    app.register_blueprint(user.blue, url_prefix="/user")

    app.run('localhost', 8801,
            True,  # 默认是False:不开启调式模式，Ture开启调试模式
            threaded=True,  # 默认是False:单线程，Ture开启多线程
            processes=1  # 默认是1个进程。不能同时开启多线程和多进程，否则会启动报错。(threaded=True,processes=2 此时会报错)
            )


```

## 路由 request response

### 1.1路由规则

```python
@blue.route('/find', methods=['GET', 'POST'])
def find():
    pass

```

请求的url是http://localhost:8801/find。路由中配置的路径就是请求的path路径。

如果使用“蓝图”则在注册时，可以注明它的url_prefix前辍。

```python
app.register_blueprint(bank.blue, url_prefix="/bank")
```

通过url_prefix参数指定某一个模块下的所有请求资源，都需要加上/bank/<子路径>
，对于/find路由来说的，应该是/bank的子路径，访问全路径是http://localhost:
8801/bank/find。

#### 1.1.1路由path中的参数

语法：

```python
@app.route('/find/<converter:word>', methods=['GET'])
def find(word):
    pass
```

converter是参数的转换器，一般是指定的类型，如string,int,float,path,uuid,any等
string是默认参数转换器  
@app.route('/find/<word>', methods=['GET'])  
这时使用的是string参数转换器

path路径中可以接收多个参数转换器  
例：

```python
@app.route('/find/<string:word>/<int:page>', methods=['GET'])
def find(word, page):
    pass
```

| Converter | Description                                      |
|-----------|--------------------------------------------------|
| string    | 	Accepts any text without a slash (the default). |
| int       | 	Accepts integers.                               |
| float     | 	Like int but for floating point values.         |
| path      | 	Like string but accepts slashes.                |

支持以下参数转换器  
"default": UnicodeConverter,  
"string": UnicodeConverter,  
"any": AnyConverter,  
"path": PathConverter,  
"int": IntegerConverter,  
"float": FloatConverter,  
"uuid": UUIDConverter,

可以配置自定义参数转换器

```python
# 1
# custom_converter.py中定义自定义参数转换器

from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):
    def __init__(self, url_map):
        super().__init__(url_map)
        self.regex = r'1[34578]\d{9}'

    # 这里处理path参数值，传参给给route函数使用
    def to_python(self, value: str):
        mobile = _Mobile(value)
        return mobile

    # 调用flask模块url_for函数时会触发此函数
    def to_url(self, value) -> str:
        return str(value).replace("4", "8")


class _Mobile:
    def __init__(self, mobile):
        self.mobile = mobile

    def __str__(self):
        return "phone:{}".format(self.mobile)


# 2
# server.py
# 注册自定义converter
app.url_map.converters['mobile'] = MobileConverter


# 3
# bank.py
# 在route中使用mobile参数转换器
@blue.route('/find_mobile/<mobile:keyword>', methods=['GET'])
def find_mobile(keyword):
    return 'type : %s , value : %s ' % (type_str(keyword), keyword)
```

```python
@app.route('/forward/<path:url>', methods=['GET'])
def forward(url):
    return redirect(url)

```

以上路由配置，对于/forward/http://www.baidu.com，是合法的，

#### 1.1.2 路由中的请求方法

路由中的请求方法是通过methods设置的，眀要求是list类型  
没有指定methods，默认值为methods=["GET","OPTIONS"]

常用的请求方法：

* GET：查询数据时使用，URL可以传的参数大小有限制，1M以内，参数显示在URL中。
* POST：添加或编辑数据时使用，可以上传超过1G的大数据，且以表单参数的方式上传并不显示在请求地址中，相比GET，请求数据更安全且支持大数据或文件。
* PUT：更新数据时使用
* PATCH：更新部分数据时使用
* DELETE：删除数据时使用

```python
@app.route('/delete/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    return "delete {}".format(bank_id)
```

#### 1.1.3 路由的反向解析

```python
@blue.route('/add/<bank_name>')
def add_card(bank_name):
    return "%s 开户成功！" % (bank_name)


@blue.route('select_bank')
def select_bank():
    bank_name = "招商银行"
    return """
    选择银行成功，3秒后<a href ="%s">进入开户页</a>
    """ % (url_for("cardBlue.add_card", bank_name=bank_name))
```

通过url_for反向解析获取url
url_for("函数名",**kwargs) 反向解析获取flask的路由注册的路径
url_for("蓝图名"."函数名",**kwargs) 反向解析指定蓝图的路由注册的路径

```python
# server.py

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
```

#### 单元测试

创建单元测试类，对重要功能进行测试

针对PUT/DELETE/POST/GET等HTTP请求接口测试，可以使用requests库

```shell
# 安装requests模块
pip install requests
```

requests库中提供相关函数，函数的名称与请求方法是一一对应，可以使用request.request()调用所有的method方法

```python
from unittest import TestCase

import requests


# 继承TestCase类
class TestBank(TestCase):

    # 声明单元测试方法
    # 方法名以test_开头
    def test_del(self):
        url = "http://localhost:8801/bank/delete_bank/100"
        method = "DELETE"
        resp = requests.request(method, url)

        self.assertIs(resp.status_code, 200, "request fail")
        print(resp.text)

```

### 1.2 请求对象 request

```python
from flask import request
```

请求对象本质上是封装客户端发送的请求数据，在flask中由werkzeug库（实现python的WSGI接口）封装的，包含请求的路径，请求头，请求方法，请求中中包含Cookies、请求参数、上传的数据。

一个请求对象中包含数据的属性一般都是dict类型。如：

* request.args查询参数，url路径中使用?和&分融的查询参数
* request.form 表单参数，一般是post请求方法包含的数据
* request.headers 请求头
* request.cookies Cookies数据
* request.files 上传的文件数据
* request.method 请求方法 方法名为字母大写
* request.url 请求的路径

request.url有几种情况：

* url   :完整的请求路径 http://localhost:8801/bank/find?bank_id=1
* base_url :去掉get参数的路径 http://localhost:8801/bank/find
* host_url :只有主机和端的路径 http://localhost:8801
* path :路由中的路径 /bank/find

### 1.3 响应对象 response   

