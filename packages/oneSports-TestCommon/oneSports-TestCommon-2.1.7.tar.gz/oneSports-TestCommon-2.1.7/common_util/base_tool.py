from datetime import datetime


class RandomStr:
    def geTimeStr(self, pre="", strf="%Y%m%d%H%M%S"):
        time_str = datetime.now().strftime(strf)
        return '{}{}'.format(pre, time_str)


class Generic:
    @classmethod
    def from_dict(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        return obj


class JsonSerializable(object):

    def toDict(self):
        for key, value in self.__dict__.items():
            if isinstance(value, JsonSerializable) and hasattr(value, 'toDict'):
                self.__dict__[key] = value.toDict()
        return self.__dict__

    def toJson(self):
        if isinstance(self, JsonSerializable) and hasattr(self, 'toDict'):
            return json.dumps(self.toDict(), ensure_ascii=False)
        else:
            return json.dumps(self.__dict__, ensure_ascii=False)