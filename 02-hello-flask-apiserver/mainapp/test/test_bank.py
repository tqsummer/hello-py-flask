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
