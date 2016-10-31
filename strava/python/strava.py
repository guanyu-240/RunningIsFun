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


# constants
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
ATHLETES_URL = "https://www.strava.com/api/v3/athletes/{}"
ACTIVITIES_URL = "https://www.strava.com/api/v3/activities/{}"
ATHLETE_ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
CLUBS_URL = "https://www.strava.com/api/v3/clubs/{}"


################################################################################
class Strava():
################################################################################
  """
  Strava access methods
  """
  def __init__(self, access_token):
    self.__accessToken = access_token
  
  """
  Basic queries
  """
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


