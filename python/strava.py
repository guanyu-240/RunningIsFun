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
from datetime import date,timedelta,datetime

# from pypi
import requests
from pytz import timezone


# url constants
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
ATHLETES_URL = "https://www.strava.com/api/v3/athletes/{}"
ACTIVITIES_URL = "https://www.strava.com/api/v3/activities/{}"
ATHLETE_ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
CLUBS_URL = "https://www.strava.com/api/v3/clubs/{}{}"

# other constants
METERS_PER_KM = 1000.0
METERS_PER_MI = 1609.0

# functions
def get_start_of_week(time_zone='UTC'):
  """
  Get the start of current week
  """
  today = datetime.now(timezone(time_zone))
  week_start = today - timedelta(today.weekday())
  return week_start.date()

def convert_datestr(date_str, time_zone='UTC'):
  """
  Format the datetime string
  """
  t = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
  t = timezone('UTC').localize(t)
  t = t.astimezone(timezone(time_zone))
  return t

def process_activity(activity, unit='mi'):
  """
  Convert the distance and calculate average pace
  """
  if unit == 'km':
    activity['distance'] = activity['distance'] / METERS_PER_KM
  else: activity['distance'] = activity['distance'] / METERS_PER_MI
  moving_time = float(activity['moving_time'])
  if activity['distance'] > 0:
    activity['avg_pace'] = moving_time / (60.0*activity['distance'])
  else:
    activity['avg_pace'] = 999
  return activity

################################################################################
class Strava():
################################################################################
  """
  Strava access methods
  """
  
  """
  Basic queries
  """
  # Methods for getting athlete information
  def getAthleteInfoSelf(self, access_token):
    """
    Get the information of self
    """
    params = {'access_token': access_token}
    r = requests.get(ATHLETE_URL, params)
    r.raise_for_status()
    return r.json()


  def getAthleteInfo(self, access_token, user_id):
    """
    Get the information of an athlete
    user_id: integer, strava id for the athlete
    """
    params = {'access_token': access_token}
    r = requests.get(ATHLETES_URL.format(user_id), params)
    r.raise_for_status()
    return r.json()


  # Methods for getting activity information
  def getAnActivity(self, access_token, activity_id):
    """
    Get the information of an activity
    activity_id: integer, activity id
    """
    params = {'access_token': access_token}
    r = requests.get(ACTIVITIESS_URL.format(activity_id), params)
    r.raise_for_status()
    return r.json()

  def listAthleteActivities(self, access_token, before=None, after=None, page=None, per_page=None):
    """
    Get a list of activities
    before:   integer, seconds since UNIX epoch
    after:    integer, seconds since UNIX epoch
    page:     integer
    per_page:	integer
    """
    params = {'access_token': access_token}
    if before: params['before'] = before
    if after: params['after'] = after
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r = requests.get(ATHLETE_ACTIVITIES_URL, params=params)
    return r.json()

  def listFriendsActivities(self, access_token, before=None, page=None, per_page=None):
    """
    Get a list of friends' activities
    before:   integer, seconds since UNIX epoch
    page:     integer
    per_page: integer
    """
    params = {'access_token': access_token}
    if before: params['before'] = before
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r = requests.get(ACTIVITIESS_URL.format('following'), params=params)
    return r.json()

  # Methods for getting club information
  def getClub(self, access_token, club_id):
    """
    Get the information of a club
    club_id: integer
    """
    params = {'access_token': access_token}
    r =  requests.get(CLUBS_URL.format(club_id, ''), params=params)
    r.raise_for_status()
    return r.json()

  def listClubMembers(self, access_token, club_id, page=None, per_page=200):
    """
    Get the list of club members
    club_id:  integer
    page:     integer
    per_page: integer
    """
    params = {'access_token': access_token}
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r =  requests.get(CLUBS_URL.format(club_id, '/members'), params=params) 
    r.raise_for_status()
    return r.json()
