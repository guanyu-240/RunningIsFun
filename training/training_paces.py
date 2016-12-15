#!/usr/bin/python
from data_structure import TrainingPace

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


