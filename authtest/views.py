from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import forget

@view_config(route_name='home', renderer='string')
def view_home(request):
    return "This is my happy home page"

@view_config(route_name='logout')
def view_logout(request):
    headers = forget(request)
    return Response(headerlist=headers, body='logged out')

@view_config(route_name='authinfo', renderer='json')
def view_authinfo(request):
    principals = request.effective_principals
    return {'principals': principals}

@view_defaults(context='authtest.entities.Thing', route_name='thing')
class ViewThing:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name='view', renderer='json', permission='view')
    def action_view(self):
        return {'action': 'view', 'entity': self.context.__json__()}

    @view_config(name='edit', renderer='json', permission='edit')
    def action_edit(self):
        return {'action': 'edit', 'entity': self.context.__json__()}

