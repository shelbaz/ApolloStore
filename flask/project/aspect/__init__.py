

class Aspect(object):

    def set(func):
        def new_func(self, id, obj):
            from project import identity_map, logger

            # Checks pre-condition
            if identity_map.hasId(id):
                logger.error('Object already in Identity Map.')
                return False
            else:
                func(self, id, obj)
                # Checks post-condition
                if identity_map.hasId(id):
                    return True
                else:
                    return False
        return new_func

    def get(func):
        def new_func(self, id):
            from project import identity_map, logger

            # Checks pre-condition
            if not identity_map.hasId(id):
                logger.error('Object not in Identity Map.')
                return False
            else:
                res = func(self, id)
                # Checks post-condition
                if identity_map.hasId(id):
                    return res
                else:
                    return False
        return new_func

    def delete(func):
        def new_func(self, id):
            from project import identity_map, logger

            # Checks pre-condition
            if not identity_map.hasId(id):
                logger.error('Object not in Identity Map.')
                return False
            else:
                func(self, id)
                # Checks post-condition
                if not identity_map.hasId(id):
                    return True
                else:
                    return False
        return new_func
