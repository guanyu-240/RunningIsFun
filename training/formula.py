#!/usr/bin/python
import math

"""
Jack Daniels Running Formula
"""
# Constants
################################################################################
MI_KM_RATIO = 1.609344

# Percent of max heart rate
PCT_LT = 0.88

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
  if unit == 'km':
    d_given /= MI_KM_RATIO
    d_target /= MI_KM_RATIO
  factor = 1.06
  if d_target <= 2.0 and d_target > 1.0: factor = 1.07
  elif d_target <= 1.0: factor = 1.08
  return t_given * math.pow(d_target/d_given, factor)


"""
Calculate VO2 of a race
params:
distance: float, in meters
time: int, in seconds
"""
def vo2(dist, time):
   dist_per_min = 60.0*dist/float(time)
   ret = -4.6 + 0.182258 * dist_per_min + 0.000104 * math.pow(dist_per_min, 2)
   return ret


"""
Percent of VO2 Max
params:
time: int, in seconds
"""
def vo2max_percent(time):
  t_minutes = float(time)/60.0
  ret = 0.8 + 0.1894393*math.exp(-0.012778*t_minutes) + \
              0.2989558*math.exp(-0.1932605*t_minutes)
  return ret

"""
Calculate VDOT
params:
distance: float
time: int, in seconds
unit: 'mi' or 'km'
"""
def vdot(dist, time, unit="mi"):
  dist *= 1000.0
  if unit == 'mi': dist *= MI_KM_RATIO
  return vo2(dist, time)/vo2max_percent(time)

"""
Calculate the corresponding training pace given % of heart rate and vdot
"""
def pace_calc(percent_HRMax, vdot, unit='mi'):
  adjusted_vdot = vdot*(0.59+0.41*(percent_HRMax-0.65)/0.35)
  pace = 1609.344*60.0 / (29.54+5.000663*adjusted_vdot - \
            0.007546*math.pow(adjusted_vdot, 2))
  if unit == 'km': pace /= 1.609344
  return int(round(pace))


