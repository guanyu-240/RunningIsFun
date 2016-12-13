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

"""
Hansons Marathon Method
"""
################################################################################
"""
Pace factors base on marathon pace
"""
HANSONS_MP_5K = 0.88
HANSONS_MP_10K = 0.9175
HANSONS_MP_LONG = 1.0925
HANSONS_MP_AE1 = 1.14
HANSONS_MP_AE2 = 1.225
HANSONS_MP_REC = 1.3075

"""
Calculate Training Paces by marathon pace
Params:
mp: Integer, marathon pace(Unit: sec/mile)
"""
def hansons_paces(mp, unit='mi'):
  lt_pace = (mp - 10 if unit == 'mi' else mp - 6)
  ret = [TrainingPace("5k", int(mp*HANSONS_MP_5K), None),
         TrainingPace("10k", int(mp*HANSONS_MP_10K), None),
         TrainingPace("LT", int(mp-10), None),
         TrainingPace("Tempo", mp, None),
         TrainingPace("LR", int(mp*HANSONS_MP_LONG), None),
         TrainingPace("EA1", int(mp*HANSONS_MP_AE1), None),
         TrainingPace("EA2", int(mp*HANSONS_MP_AE2), None),
         TrainingPace("RC", int(mp*HANSONS_MP_REC), None)]
  return ret


"""
Advanced Marathoning
"""
################################################################################
