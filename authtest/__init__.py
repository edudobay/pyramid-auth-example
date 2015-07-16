from pyramid.config import Configurator
from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy

    authn_policy = AuthTktAuthenticationPolicy('abcdef123456', hashalg='sha512', callback=user_groups)
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_subscriber(handle_request, 'pyramid.events.NewRequest')

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

def handle_request(event):
    request = event.request
    if 'token' in request.GET:
        username = request.GET.pop('token')
        headers = remember(request, username)
        # generates a redirect to the same url but without the token (else we would enter an infinite loop...)
        raise HTTPFound(headers=headers, location=request.path_qs)

