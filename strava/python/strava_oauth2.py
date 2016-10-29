import urllib
import ConfigParser

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorizei?{}"

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
    auth_cfg = ConfigParser.RawConfigParser()
    auth_cfg.read(cfg_file)
    return auth_cfg

  def auth_url(self):
    params_list = (('client_id', self.__clientID), \
              ('redirect_uri', self.__redirectURI), \
              ('response_type', 'code'), \
              ('scope', 'write'), \
              ('state', 'mystate'), \
              ('approval_prompt', 'force'))
    params = urllib.urlencode(params_list, doseq=True)
    return STRAVA_AUTH_URL.format(params)
