========
fboauth2
========

Bare minimum Facebook OAuth2 client

-----
Usage
-----
::
    from fboauth2 import FBClient
    fbclient = FBClient(CLIENT_ID, CLIENT_SECRET, scope='publish_stream',
                        redirect_uri='http://example.com/callback')
    # Point users to auth url
    redirect(fbclient.get_auth_url())
    # Pass code to get access token
    code = params['code']
    access_token = fbclient.get_access_token(code)
    # Make graph requests
    me = fbclient.graph_request('me')
    print me['name']

-------
License
-------
http://marksteve.mit-license.org/