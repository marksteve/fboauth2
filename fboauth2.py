import requests
import urllib
import urlparse

try:
  import json
except ImportError:
  import simplejson as json


class FBClient(object):

  auth_uri = 'https://www.facebook.com/dialog/oauth'
  access_token_uri = 'https://graph.facebook.com/oauth/access_token'
  graph_api_uri = 'https://graph.facebook.com'

  def __init__(self, client_id, client_secret, scope=None, redirect_uri=None):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri
    self.scope = scope
    self.access_token = None

  def get_auth_url(self, scope=None, redirect_uri=None, state=None):
    if redirect_uri:
      self.redirect_uri = redirect_uri
    params = {
        'client_id': self.client_id,
        'redirect_uri': self.redirect_uri,
        'scope': scope or self.scope,
      }
    if state:
      params['state'] = state
    return self.auth_uri + '?' + urllib.urlencode(params)

  def get_access_token(self, code):
    params = {
        'client_id': self.client_id,
        'redirect_uri': self.redirect_uri,
        'client_secret': self.client_secret,
        'code': code,
      }

    response = requests.get(self.access_token_uri + '?' + urllib.urlencode(params))

    if response.ok:
      parsed_response = dict(urlparse.parse_qsl(response.content))
      access_token = self.access_token = parsed_response['access_token']
      return access_token

    else:
      error = json.loads(response.content)
      raise Exception('%s: %s' % (error['type'], error['message']))

  def graph_request(self, path):
    if self.access_token:
      path = path.lstrip('/')
      qs = urllib.urlencode({'access_token': self.access_token})
      # TODO: Handle HTTP errors
      response = requests.get('%s/%s?%s' % (self.graph_api_uri, path, qs))
      return json.loads(response.content)

    else:
      raise Exception('Not yet authorized.')
