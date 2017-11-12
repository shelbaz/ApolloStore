
from project.aspect import Aspect


class IdentityMap():

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