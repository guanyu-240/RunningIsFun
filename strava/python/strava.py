#!/usr/bin/python
################################################################################
# strava - strava API wrapped in Python

#  Copyright 2016 Guanyu Wang
################################################################################

# standard imports
import os
import ConfigParser
import urllib
import json

# from pypi
import requests
from oauth2client.client import OAuth2WebServerFlow


# constants
AUTHENTICATION_URL = "https://www.strava.com/oauth/authorize"
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
ATHLETES_URL = "https://www.strava.com/api/v3/athletes/{}"
ACTIVITIES_URL = "https://www.strava.com/api/v3/activities/{}"
ATHLETE_ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
CLUBS_URL = "https://www.strava.com/api/v3/clubs/{}"


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
    self.__requestAuthentication()

  def __getAuthConfig(self, cfg_file):
    auth_cfg = ConfigParser.RawConfigParser()
    auth_cfg.read(cfg_file)
    return auth_cfg

  def __requestAuthentication(self):
    params = {'client_id': self.__clientID, \
              'redirect_uri': self.__redirectURI, \
              'response_type': 'code', \
              'scope': 'write', \
              'state': 'mystate', \
              'approval_prompt': 'force'}
    r = requests.get(AUTHENTICATION_URL, params)
    r.raise_for_status()

  def setAccessToken(self, access_token):
    self.__accessToken = access_token

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

  def listAthleteActivities(self, before, after, page, per_page):
    """
    Get a list of activities
    """
    params = {'access_token': self.__accessToken}
    if before: params['before'] = before
    if after: params['after'] = after
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r = requests.get(ATHLETE_ACTIVITIES_URL, params)
    return r.json()


  # Methods for getting club information
  def getClub(self, club_id):
    """
    Get the information of a club
    """
    params = {'access_token': self.__accessToken}
    r =  requests.get(CLUBS_URL.format(club_id), params)
    r.raise_for_status()
    return r.json()


