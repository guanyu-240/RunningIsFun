# standard imports
import os
import ConfigParser
import urllib

# from pypi
import requests

class Strava():
  def __init__(self, cfg_file):
    auth_cfg = self.__getAuthConfig(cfg_file)
    self.__clientID = auth_cfg.getint("user", "client_id")
    self.__redirectURI = auth_cfg.get("user", "redirect_uri")
    self.__secretKey = auth_cfg.get("user", "secret_key")
    self.__accessToken = auth_cfg.get("user", "access_token")

  def __getAuthConfig(self, cfg_file):
    auth_cfg = ConfigParser.RawConfigParser()
    auth_cfg.read(cfg_file)
    return auth_cfg

  def getAthleteInfoSelf(self):
    """
    Get the information of self
    """
    url = "https://www.strava.com/api/v3/athlete"
    params = {'access_token': self.__accessToken}
    r = requests.get(url, params)
    r.raise_for_status()
    return r.json()

  def getAthleteInfo(self, user_id):
    """
    Get the information of an athlete
    user_id: strava id for the athlete
    """
    url = "https://www.strava.com/api/v3/athlete"
    params = {'access_token': self.__accessToken}
    r = requests.get(url, params)
    r.raise_for_status()
    return r.json()

