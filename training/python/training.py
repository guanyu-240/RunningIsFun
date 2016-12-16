#!/usr/bin/python
from formula import MI_KM_RATIO, time_eq, vdot, pace_calc
import xml.etree.ElementTree as ET
"""
Data structures
"""
################################################################################

MARATHON_KM = 42.195
MARATHON_MI = 26.2188
MI_KM_RATIO = 1.609344


RULE_BY_HRMAX = "1"
RULE_BY_VO2MAX = "2"
RULE_BY_RACE_PACE = "3"
RULE_BY_MP = "4"


def pace_str(seconds):
  return "{}:{:02d}".format(seconds/60, seconds%60)


class Training:
  """
  Training course class
  training: str, training name
  desc: str description of the training
  paces: paces used in the training
  """
  def __init__(self, ele):
    self.name = ele.get('name')
    self.desc = ele.find('desc').text
    self.paces = []
    for pace_ele in ele.findall('pace'):
      self.paces.append(Pace(pace_ele))

  def calculate(self, dist, time, unit='mi'):
    """
    Calculate Training Pace by a given race result
    In Hansons training methods, training paces are race paces for
    tempo, strength and VO2max
    Params:
    dist: float, race distance
    time: integer, race time in seconds
    unit: 'mi' or 'km'
    """
    pace_str_list = []
    for p in self.paces: 
      pace_str_list.append(pace_str(p.calculate_pace(dist, time, unit)))
    pace_str_for_ret = ''
    if len(pace_str_list) > 0: pace_str_for_ret += pace_str_list[0]
    if len(pace_str_list) > 1: pace_str_for_ret += ' - ' + pace_str_list[1]
    ret = {'name': self.name,
           'desc': self.desc,
           'pace': ' - '.join(pace_str_list)}
    return ret

class Pace:
  """
  Training pace class
  rule: str, pace calculation rule
  value: value used in the above rule
  op: operator used in the rule
  """
  def __init__(self, ele):
    self.rule = ele.get('rule')
    self.value = float(ele.get('value'))
    self.op = ele.get('op')

  def calculate_pace(self, dist, time, unit='mi'):
    """
    Calculate Training Paces by a given race result
    In Hansons training methods, training paces are race paces for
    tempo, strength and VO2max
    Params:
    dist: float, race distance
    time: integer, race time in seconds
    unit: 'mi' or 'km'
    """
    vd = vdot(dist, time, unit)
    ratio = (MI_KM_RATIO if unit == 'mi' else 1)
    dist_km = dist
    if unit == 'mi': dist_km *= MI_KM_RATIO
    time_marathon = time_eq(time, dist_km, MARATHON_KM, 'km')
    mp = time_marathon/MARATHON_KM
    pace = 0
    if self.rule == RULE_BY_HRMAX:
      pace = pace_calc(self.value, vd, unit)
    elif self.rule == RULE_BY_VO2MAX:
      pace = pace_calc(self.value, vd, unit, 'vo2max')
    elif self.rule == RULE_BY_RACE_PACE:
      race_time = time_eq(time, dist_km, self.value, 'km')
      pace = int(round((race_time/self.value)*ratio))
    elif self.rule == RULE_BY_MP:
      if self.op is None: pace = mp*ratio
      elif self.op == '+': pace = mp*ratio + self.value
      elif self.op == '-': pace = mp*ratio - self.value
      elif self.op == '*': pace = mp*ratio * self.value
      elif self.op == '/': pace = mp*ratio / self.value
      else: pace = mp*ratio
      if unit == 'km': pace = pace / ratio
      pace = int(round(pace))
    return pace


class TrainingPlan:
  """
  Training plan class
  name: str, training plan name
  trainings: training courses in the plan
  """
  def __init__(self, plan_ele):
    self.name = plan_ele.get('name')
    self.trainings = []
    training_root = plan_ele.find('trainings')
    for training_ele in training_root.findall('training'):
      self.trainings.append(Training(training_ele))

  def calculate(self, dist, time, unit='mi'):
    """
    Calculate Training Paces by a given race result
    In Hansons training methods, training paces are race paces for
    tempo, strength and VO2max
    Params:
    dist: float, race distance
    time: integer, race time in seconds
    unit: 'mi' or 'km'
    """
    ret = []
    for t in self.trainings:
      ret.append(t.calculate(dist, time, unit))
    return ret

def loadTrainingPlans(xml_file):
  tree = ET.parse(xml_file)
  root = tree.getroot()
  ret = {} 
  for plan_ele in root:
    ret[plan_ele.get('name')] = TrainingPlan(plan_ele)
  return ret
