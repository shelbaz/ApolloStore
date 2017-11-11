
from project.aspect import Aspect


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IdentityMap(metaclass=Singleton):

    def __init__(self):
        self.dict = {}

    def hasId(self, id):
        return id in self.dict

    @Aspect.set
    def set(self, id, object):
        self.dict[id] = object

    @Aspect.get
    def getObject(self, id):
        return self.dict[id]

    @Aspect.delete
    def delete(self, id):
        del self.dict[id]
