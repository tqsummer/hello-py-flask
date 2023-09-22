from flask import Flask
from flask import request, render_template

app = Flask(__name__, template_folder="template")


@app.route("/myFirstPage", methods=["GET", "POST"])
def myFirstPage():
    data = {
        "name": "fxq",
        "age": "41"
    }
    return render_template("myFirstPage.html", **data)


app.run('localhost', 8801,
        True,  # 默认是False:不开启调式模式，Ture开启调试模式
        threaded=True,  # 默认是False:单线程，Ture开启多线程
        processes=1  # 默认是1个进程。不能同时开启多线程和多进程，否则会启动报错。(threaded=True,processes=2 此时会报错)
        )

import random

random.randint(3,9)