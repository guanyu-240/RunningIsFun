#!/usr/bin/python
import math

"""
Jack Daniels Running Formula
"""
################################################################################
MI_KM_RATIO = 1.609344
"""
Given a race time or race goal time, get the equivalant time of
a race of another distance
Exp: Marathon - 3:00:00 => Half Marathon - ?
Params:
t_given: Integer, race time in seconds
d_given: Float, race distance
d_target: Float, distance of the race to be predicted
unit: 'mi' or 'km'
"""
def time_eq(t_given, d_given, d_target, unit='mi'):
  if unit == km:
    d_given /= MI_KM_RATIO
    d_target /= MI_KM_RATIO
  factor = 1.06
  if d_target <= 2.0 and d_target > 1.0: factor = 1.07
  elif d_target <= 1.0: factor = 1.08
  return t_given * math.pow(d_target/d_given, factor)

