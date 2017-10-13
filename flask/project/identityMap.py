class IdentityMap():
    def __init__(self):
        self.dict = {}
        
    def set(self, id, object):
        self.dict[id] = object
        
    def hasId(self, id):
        return id in self.dict
        
    def getObject(self, id):
        if self.hasId(id):
            return self.dict[id]