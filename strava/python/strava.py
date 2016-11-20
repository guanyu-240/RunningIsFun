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


# constants
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
ATHLETES_URL = "https://www.strava.com/api/v3/athletes/{}"
ACTIVITIES_URL = "https://www.strava.com/api/v3/activities/{}"
ATHLETE_ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
CLUBS_URL = "https://www.strava.com/api/v3/clubs/{}{}"

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
  Convert the distance and pace
  """
  if unit == 'km':
    activity['distance'] = activity['distance']/1000.0
  else: activity['distance'] = activity['distance']/1609.0
  activity['avg_pace'] = 60.0*activity['distance']/float(activity['moving_time'])
  return activity

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
    user_id: integer, strava id for the athlete
    """
    params = {'access_token': self.__accessToken}
    r = requests.get(ATHLETES_URL.format(user_id), params)
    r.raise_for_status()
    return r.json()


  # Methods for getting activity information
  def getAnActivity(self, activity_id):
    """
    Get the information of an activity
    activity_id: integer, activity id
    """
    params = {'access_token': self.__accessToken}
    r = requests.get(ACTIVITIESS_URL.format(activity_id), params)
    r.raise_for_status()
    return r.json()

  def listAthleteActivities(self, before=None, after=None, page=None, per_page=None):
    """
    Get a list of activities
    before:   integer, seconds since UNIX epoch
    after:    integer, seconds since UNIX epoch
    page:     integer
    per_page:	integer
    """
    params = {'access_token': self.__accessToken}
    if before: params['before'] = before
    if after: params['after'] = after
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r = requests.get(ATHLETE_ACTIVITIES_URL, params=params)
    return r.json()

  def listFriendsActivities(self, before=None, page=None, per_page=None):
    """
    Get a list of friends' activities
    before:   integer, seconds since UNIX epoch
    page:     integer
    per_page: integer
    """
    params = {'access_token': self.__accessToken}
    if before: params['before'] = before
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r = requests.get(ACTIVITIESS_URL.format('following'), params=params)
    return r.json()

  # Methods for getting club information
  def getClub(self, club_id):
    """
    Get the information of a club
    club_id: integer
    """
    params = {'access_token': self.__accessToken}
    r =  requests.get(CLUBS_URL.format(club_id, ''), params=params)
    r.raise_for_status()
    return r.json()

  def listClubMembers(self, club_id, page=None, per_page=200):
    """
    Get the list of club members
    club_id:  integer
    page:     integer
    per_page: integer
    """
    params = {'access_token': self.__accessToken}
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r =  requests.get(CLUBS_URL.format(club_id, '/members'), params=params) 
    r.raise_for_status()
    return r.json()

  def getClubActivities(self, club_id, before=None, page=None, per_page=None, time_zone='UTC'):
    """
    Get the list of club activities
    before:   integer, seconds since UNIX epoch
    page:     integer
    per_page: integer
    """
    params = {'access_token': self.__accessToken}
    if before: params['before'] = before
    if page: params['page'] = page
    if per_page: params['per_page'] = per_page
    r =  requests.get(CLUBS_URL.format(club_id, '/activities'), params=params)
    r.raise_for_status()
    ret = r.json()
    for x in ret:
      x['start_date'] = convert_datestr(x['start_date'], time_zone)
    return ret

  """
  Commonly used complex queries
  """
  def getClubActivitiesCurWeek(self, club_id, time_zone='UTC'):
    """
    Get the list of club activities in the current week
    club_id: integer
    """
    club_activities = self.getClubActivities(club_id, per_page=200, time_zone=time_zone)
    week_start = get_start_of_week(time_zone)
    club_activities_curweek = filter( \
            lambda x: x['start_date'].date() >= week_start and \
                      x['type'] == 'Run', \
            club_activities)
    return club_activities_curweek

  def getClubActivitiesToday(self, club_id, time_zone='UTC'):
    """
    Get the list of club activities today
    club_id: integer
    """
    club_activities = self.getClubActivities(club_id, per_page=50, time_zone=time_zone)
    week_start = get_start_of_week()
    club_activities_curweek = filter( \
            lambda x: x['start_date'].date() >= date.today() and \
                      x['type'] == 'Run', \
            club_activities)
    return club_activities_curweek
