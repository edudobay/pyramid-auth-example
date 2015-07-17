from pyramid.config import Configurator
from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound

def remember_callback(request, response):
    if request.authenticated_userid is None: return
    extra_headers = remember(request, request.authenticated_userid)
    response.headerlist.extend(extra_headers)

from pyramid.authentication import AuthTktAuthenticationPolicy
class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def unauthenticated_userid(self, request):
        if 'token' in request.GET:
            username = request.GET.pop('token')
            request.add_response_callback(remember_callback)
            request._unauthenticated_userid = username
            return username

        # We must really keep the first time apart or else the callback will be
        # added multiple times
        elif hasattr(request, '_unauthenticated_userid'):
            return request._unauthenticated_userid

        # fall back to parent's algorithm
        return super().unauthenticated_userid(request)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    from pyramid.authorization import ACLAuthorizationPolicy

    authn_policy = MyAuthenticationPolicy('abcdef123456', hashalg='sha512', callback=user_groups)
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.add_route('authinfo', '/info')
    config.add_route('thing', '/thing/*traverse', factory='authtest.entities.ThingFactory')

    config.scan()
    return config.make_wsgi_app()

def user_groups(username, request):
    # usernames beginning with an 'a' refer to admin users
    if username.startswith('a'):
        return ['group:admin']
    return []

