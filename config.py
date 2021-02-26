from os import environ
import json


config_path = "./config.json"


class JSONProvider: 
    def __init__(self, path):
        with open(path, "r") as f:
            self.__config = json.load(f)

    def get(self, *args):
        data = self.__config[args[0]]
        for i in range(1, len(args), 1):
            data = data[args[i]]
        return data


class DBProvider(JSONProvider):
    def __init__(self, path):
        super().__init__(path)
        self.host = self.get("DB", "host")
        self.username = self.get("DB", "username")
        self.password = self.get("DB", "password")
        self.db = self.get("DB", "db")
        self.charset = self.get("DB", "charset")


class BOTProvider(JSONProvider):
    def __init__(self, path):
        super().__init__(path)
        self.TOKEN = self.get("BOT", "TOKEN")
        self.webhook_url = 'https://%s.herokuapp.com/hook' % environ.get(self.get("BOT", "WEBHOOK_URL"))


var_DBProvider = DBProvider(config_path)
var_BOTProvider = BOTProvider(config_path)

conargs = {
    'host': var_DBProvider.host,
    'user': var_DBProvider.username,
    'password': var_DBProvider.password,
    'db': var_DBProvider.db,
    'charset': var_DBProvider.charset
}

webhook_url = var_BOTProvider.webhook_url
BOT_API = var_BOTProvider.TOKEN