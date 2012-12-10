import requests
import urllib
import urlparse


class FBClient(object):

    auth_uri = 'https://www.facebook.com/dialog/oauth'
    access_token_uri = 'https://graph.facebook.com/oauth/access_token'
    graph_api_uri = 'https://graph.facebook.com'

    def __init__(self, client_id, client_secret, scope=None, redirect_uri=None,
                 access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.access_token = access_token

    def get_auth_url(self, scope=None, redirect_uri=None, state=None):
        if redirect_uri:
            self.redirect_uri = redirect_uri
        params = dict(client_id=self.client_id,
                      redirect_uri=self.redirect_uri,
                      scope=scope or self.scope or '')
        if state:
            params['state'] = state
        return self.auth_uri + '?' + urllib.urlencode(params)

    def get_access_token(self, code):
        params = dict(client_id=self.client_id,
                      client_secret=self.client_secret,
                      redirect_uri=self.redirect_uri,
                      code=code)

        response = requests.get(self.access_token_uri, params=params)

        if response.ok:
            parsed_response = dict(urlparse.parse_qsl(response.content))
            access_token = self.access_token = parsed_response['access_token']
            return access_token

        else:
            try:
                error = response.json.get('error')
                if error:
                    error_type = error.get('type')
                    error_message = error.get('message')
                    if error_type and error_message:
                        raise Exception('%s: %s' % (error_type, error_message))
            except ValueError:  # Invalid JSON
                pass
            except AttributeError:  # Not a dict
                pass
            raise Exception("An unknown error has occurred: %s" %
                            response.content)

    def request(self, uri, method='get', **req_kwargs):
        if self.access_token:
            method = method.lower()

            if method in ('get', 'options'):
                req_kwargs['allow_redirects'] = True
            elif method == 'head':
                req_kwargs['allow_redirects'] = False

            params = req_kwargs.setdefault('params', {})
            params['access_token'] = self.access_token

            # TODO: Handle HTTP errors
            response = requests.request(method, uri, **req_kwargs)

            return response.json

        else:
            raise Exception('Not yet authorized.')

    def graph_request(self, path, *args, **kwargs):
        path = path.lstrip('/')
        uri = '%s/%s' % (self.graph_api_uri, path)
        return self.request(uri, *args, **kwargs)
