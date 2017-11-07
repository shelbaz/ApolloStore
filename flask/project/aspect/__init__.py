
from project.identityMap import IdentityMap

class Aspect(object):

    def set(func):
        def new_func(x):

            res = func(x)
            print 'Returning output value : %s' % res
            return res
        return new_func
