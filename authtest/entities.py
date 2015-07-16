from pyramid.security import Allow, Everyone, Authenticated

class Thing:
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'group:admin', 'edit'),
    ]

    def __json__(self):
        return {'type': 'Thing', 'id': int(self.id)}

    def __repr__(self):
        return '<Thing #%d>' % self.id

class ThingFactory:

    def __init__(self, request):
        # self.request = request
        pass

    def __getitem__(self, key):
        i = Thing()
        i.id = int(key)
        print(i)
        return i

