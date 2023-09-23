from mainapp.dao import BaseDao


class BankDao(BaseDao):
    def find_all(self):
        return super().find_all("bank", )
