#!/usr/bin/python

"""
Data structures
"""
################################################################################

MARATHON_KM = 42.195
MARATHON_MI = 26.2188

def pace_str(seconds):
  return "{}:{:02d}".format(seconds/60, seconds%60)

class TrainingPace:
  """
  Training pace class
  training: str, training name
  pace1: int, training pace in seconds
  pace2: int, training pace in seconds, 
         the max pace if the training pace is in a range
  """
  def __init__(self, training, pace1, pace2):
    self.training = training
    self.pace1 = pace1
    self.pace2 = pace2

  def toStr(self):
    pace_part = pace_str(self.pace1) if self.pace2 is None else \
               "{} - {}".format(pace_str(self.pace1), pace_str(self.pace2))
    return "{}: {}".format(self.training, pace_part)

