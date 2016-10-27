#!/usr/bin/python
################################################################################
# strava - strava API wrapped in Python

#  Copyright 2016 Guanyu Wang
################################################################################

# standard imports
import os
import ConfigParser
import urllib

# from pypi
import requests


# constants
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
ATHLETES_URL = "https://www.strava.com/api/v3/athlete/{}"
ACTIVITIES_URL = "https://www.strava.com/api/v3/activities{}"

################################################################################
class Strava():
################################################################################
  '''
  Strava access methods
  '''

  def __init__(self, cfg_file):
    """
    Initialize, takes authorization config file
    Format:
    [strava_api]
    client_id=<client id obtained after app registration>
    redirect_uri=<URL to which the user will be redirected with the auth code>
    secret_key=<secret key obtained after app registration>
    accessToken=<access token obtained after app registration or authorization>
    """
    auth_cfg = self.__getAuthConfig(cfg_file)
    self.__clientID = auth_cfg.getint("strava_api", "client_id")
    self.__redirectURI = auth_cfg.get("strava_api", "redirect_uri")
    self.__secretKey = auth_cfg.get("strava_api", "secret_key")
    self.__accessToken = auth_cfg.get("strava_api", "access_token")

  def __getAuthConfig(self, cfg_file):
    auth_cfg = ConfigParser.RawConfigParser()
    auth_cfg.read(cfg_file)
    return auth_cfg


  # Methods for getting athlete information
  def getAthleteInfoSelf(self):
    """
    Get the information of self
    """
    params = {'access_token': self.__accessToken}
    r = requests.get(ATHLETE_URL, params)
    r.raise_for_status()
    return r.json()


  def getAthleteInfo(self, user_id):
    """
    Get the information of an athlete
    user_id: strava id for the athlete
    """
    params = {'access_token': self.__accessToken}
    r = requests.get(ATHLETES_URL.format(user_id), params)
    r.raise_for_status()
    return r.json()


  # Methods for getting activity information
  def getAnActivity(self, activity_id):
    """
    Get the information of an activity
    """
    params = {'access_token': self.__accessToken}
    r = requests.get(ACTIVITIESS_URL.format(activity_id), params)
    r.raise_for_status()
    return r.json()
