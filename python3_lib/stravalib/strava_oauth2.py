################################################################################
# StravaAuth
# Methods of strava API authentication
#
################################################################################
# standard imports
import urllib.request, urllib.parse, urllib.error
import configparser
# pypi
import requests


STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize?{}"
STRAVA_AUTHTOKEN_URL = "https://www.strava.com/oauth/token"

class StravaAuth():

  def __init__(self, cfg_file):
    """
    Initialize, takes authorization config file
    Format,
    [strava_api]
    client_id=<client id obtained after app registration>
    redirect_uri=<URL to which the user will be redirected with the auth code>
    client_secret=<client secret obtained after app registration>
    accessToken=<access token obtained after app registration or authorization>
    """
    auth_cfg = self.__getAuthConfig(cfg_file)
    self.__clientID = auth_cfg.getint("strava_api", "client_id")
    self.__redirectURI = auth_cfg.get("strava_api", "redirect_uri")
    self.__clientSecret = auth_cfg.get("strava_api", "client_secret")

  def __getAuthConfig(self, cfg_file):
    auth_cfg = configparser.RawConfigParser()
    auth_cfg.read(cfg_file)
    return auth_cfg

  def auth_url(self):
    """
    Return the authentication URL with parameters
    """
    params_list = (('client_id', self.__clientID), \
              ('redirect_uri', self.__redirectURI), \
              ('response_type', 'code'), \
              ('scope', 'activity:read_all'), \
              ('state', 'mystate'), \
              ('approval_prompt', 'force'))
    params = urllib.parse.urlencode(params_list, doseq=True)
    return STRAVA_AUTH_URL.format(params)

  def token_exchange(self, auth_code):
    """
    Get the token exchange
    """
    params = {'client_id': self.__clientID, \
              'client_secret': self.__clientSecret, \
              'code': auth_code}
    r = requests.post(STRAVA_AUTHTOKEN_URL, data=params)
    #r.raise_for_status()
    return r.json()

  def refresh_token(self, refresh_token):
    """
    Refresh access token
    """
    params = {'client_id': self.__clientID, \
              'client_secret': self.__clientSecret, \
              'grant_type': 'refresh_token', \
              'refresh_token': refresh_token}
    r = requests.post(STRAVA_AUTHTOKEN_URL, data=params)
    #r.raise_for_status()
    return r.json()
