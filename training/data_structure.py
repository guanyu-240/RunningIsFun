#!/usr/bin/python

def pace_str(seconds):
  return "{}:{:02d}".format(seconds/60, seconds%60)

class TrainingPace:
  def __init__(self, training, pace1, pace2):
    self.training = training
    self.pace1 = pace1
    self.pace2 = pace2

  def toStr(self):
    pace_part = pace_str(self.pace1) if self.pace2 is None else \
               "{} - {}".format(pace_str(self.pace1), pace_str(self.pace2))
    return "{}: {}".format(self.training, pace_part)

