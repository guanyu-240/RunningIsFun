#!/usr/bin/python
from data_structure import MARATHON_KM, TrainingPace
from formula import MI_KM_RATIO, time_eq, vdot, pace_calc

"""
Hansons Marathon Method
"""
################################################################################

PCT_RECOVERY = 0.65
PCT_EA1 = 0.693
PCT_EA2 = 0.743
PCT_MA = 0.775

"""
Calculate Training Paces by a given race result
In Hansons training methods, training paces are race paces for
tempo, strength and VO2max
Params:
dist: float, race distance
time: integer, race time in seconds
unit: 'mi' or 'km'
"""

def hansons_paces(dist, time, unit='mi'):
  # calculate equivalent 5k, 10k and marathon paces
  dist_km = dist
  if unit == 'mi': dist_km *= MI_KM_RATIO
  time_5k = time_eq(time, dist_km, 5.0, 'km')
  time_10k = time_eq(time, dist_km, 10.0, 'km')
  time_marathon = time_eq(time, dist_km, MARATHON_KM, 'km')
  ratio = (MI_KM_RATIO if unit == 'mi' else 1)
  pace_5k = int(round((time_5k/5.0)*ratio))
  pace_10k = int(round((time_10k/10.0)*ratio))
  mp = int(round((time_marathon/MARATHON_KM)*ratio))
  # calculate easy run paces
  vd = vdot(dist, time, unit)
  pace_recovery = pace_calc(PCT_RECOVERY, vd, unit='mi')
  pace_ea_1 = pace_calc(PCT_EA1, vd, unit='mi')
  pace_ea_2 = pace_calc(PCT_EA2, vd, unit='mi')
  pace_ma = pace_calc(PCT_MA, vd, unit='mi')
  ret = [TrainingPace("5k", pace_5k, None),
         TrainingPace("10k", pace_10k, None),
         TrainingPace("Strength", mp-10, None),
         TrainingPace("Tempo", mp, None),
         TrainingPace("Long", pace_ma, None),
         TrainingPace("Easy Aerobic B", pace_ea_2, None),
         TrainingPace("Easy Aerobic A", pace_ea_1, None),
         TrainingPace("Recovery", pace_recovery, None)]
  return ret


"""
Advanced Marathoning
"""
################################################################################
"""
Calculate Training Paces by marathon goal time
In Advanced Marathoning, Lactate threshold and VO2max are based on race paces.
Long Run pace is based on the goal marathon pace
Params:
time: integer, race time in seconds
unit: 'mi' or 'km'
"""

def am_paces(time, unit='mi'):
  time_5k = time_eq(time, MARATHON_KM, 5.0, 'km')
  time_15k = time_eq(time, MARATHON_KM, 15.0, 'km')
  time_half = time_eq(time, MARATHON_KM, MARATHON_KM/2.0, 'km')
  ratio = (MI_KM_RATIO if unit == 'mi' else 1)
  mp = int(round((time/MARATHON_KM)*ratio))
  pace_5k = int(round((time_5k/5.0)*ratio))
  pace_15k = int(round((time_15k/15.0)*ratio))
  hmp = int(round((2*time_half/MARATHON_KM)*ratio))
  ret = [TrainingPace("VO2Max", pace_5k, None),
         TrainingPace("LT_Fast", pace_15k, None),
         TrainingPace("LT_Slow", hmp, None),
         TrainingPace("Long", int(round(mp*1.2)), int(round(mp*1.1)))]
  return ret
