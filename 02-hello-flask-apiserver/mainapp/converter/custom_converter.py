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


if __name__ == '__main__':
    pass
