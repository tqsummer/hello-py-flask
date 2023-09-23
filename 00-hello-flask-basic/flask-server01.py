import urllib

from flask import Flask
from flask import request, render_template, redirect, url_for

from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):
    def __init__(self, url_map):
        super().__init__(url_map)
        self.regex = r'1[34578]\d{9}'

    def to_python(self, value: str):
        return 'm:{}'.format(value)

    def to_url(self, value) -> str:
        print("value")
        return "13123456789"


class SplitSearchPath(BaseConverter):
    def __init__(self, url_map, separator='+'):
        super().__init__(url_map)
        self.separator = urllib.parse.unquote(separator)

    def to_python(self, url):
        return url.split(self.separator)

    def to_url(self, elements):
        print(elements)
        for e in elements:
            print(super().to_url(e))
        a = [super(SplitSearchPath, self).to_url(e) for e in elements]
        print(a)
        return self.separator.join(super(SplitSearchPath, self).to_url(e)
                                   for e in elements)


app = Flask(__name__, template_folder="template")
app.url_map.converters['mobile'] = MobileConverter
app.url_map.converters['ssp'] = SplitSearchPath


@app.route("/myFirstPage", methods=["GET", "POST"])
def myFirstPage():
    data = {
        "name": "fxq",
        "age": "41"
    }
    return render_template("myFirstPage.html", **data)


@app.route("/find/<int:id>", methods=["GET"])
def find(id):
    return "find id: %s" % (id,)


@app.route("/find_mobile/<mobile:keyword>", methods=["GET"])
def find_mobile(keyword):
    return "find mobile: %s" % (keyword,)


@app.route("/find_ssp/<ssp:keyword>", methods=["GET"])
def find_ssp(keyword):
    return "find ssp: %s" % (keyword,)


@app.route("/find_ssp_redirect/<keyword1>", methods=["GET"])
def find_ssp_redirect(keyword1):
    print(url_for('find_ssp', keyword=keyword1))
    return "abv"


if __name__ == '__main__':
    app.run('localhost', 8801,
            True,  # 默认是False:不开启调式模式，Ture开启调试模式
            threaded=True,  # 默认是False:单线程，Ture开启多线程
            processes=1  # 默认是1个进程。不能同时开启多线程和多进程，否则会启动报错。(threaded=True,processes=2 此时会报错)
            )
