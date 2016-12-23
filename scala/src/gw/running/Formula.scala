package gw.running
import Unit._;


object Formula {
  val MI_KM_RATIO : Double = 1.609344
  
  /*
   * Given a race time or race goal time, get the equivalant time of
   * a race of another distance
   * Exp: Marathon - 3:00:00 => Half Marathon - ?
   * Params:
   * t_given: Integer, race time in seconds
   * d_given: Double, race distance
   * d_target: Double, distance of the race to be predicted
   * unit: Unit, MI or KM
   */
  def time_eq(time_given : Int, dist_given : Double, 
              dist_target : Double, unit : Unit) : Int = {
    var (d_given, d_target) = (dist_given, dist_target)
    if (unit == MI) {
      d_given /= MI_KM_RATIO
      d_target /= MI_KM_RATIO
    }
    var factor = 1.06
    if (d_target <= 2.0 && d_target > 1.0)  factor = 1.07 
    else if( d_target <= 1.0) factor = 1.08
    return time_given * math.pow(d_target/d_given, factor).asInstanceOf[Int]
  }

  /*
   * Calculate VO2 of a race
   * Params:
   * distance: Double, in meters
   * time: Int, in seconds
   */
  def vo2(dist : Double, time : Int) : Double = {
    val dist_per_min = 60.0*dist/time.asInstanceOf[Double]
    val ret : Double = -4.6 + 0.182258 * dist_per_min + 0.000104 * math.pow(dist_per_min, 2)
    return ret
  }

  /*
   * Percent of VO2 Max given a race time
   * Parameters:
   * time: Int, in seconds
   */
  def vo2max_percent(time: Int) : Double = {
    val t_minutes = time.asInstanceOf[Double]/60.0
    val ret : Double = 0.8 + 0.1894393*math.exp(-0.012778*t_minutes) + 
              0.2989558*math.exp(-0.1932605*t_minutes)
    return ret
  }
  
  /* 
   * Calculate VDOT
   * Params:
   * distance: Double
   * time: Int, in seconds
   * unit: Unit, MI or KM
   */
  def vdot(distance : Double, time : Int, unit : Unit): Double = {
    var dist = distance*1000.0
    if (unit == MI) dist *= MI_KM_RATIO
    return vo2(dist, time)/vo2max_percent(time)
  }
  
  /*
   * Calculate the corresponding training pace given % of heart rate and vdot
   * Params:
   * percent_max: Double, percentage of vo2max
   * vdot: Double, vdot value
   */
  def pace_calc(percent_max : Double, vdot : Double, unit : Unit): Int = {
    val adjusted_vdot = vdot*percent_max
    var pace = 1609.344*60.0 / (29.54+5.000663*adjusted_vdot - 
               0.007546*math.pow(adjusted_vdot, 2))
    if (unit == KM) pace /= 1.609344
    return math.ceil(pace).toInt
  }
  
  /*
   * Convert % of max heart rate to % of vo2max
   */
  def convertToPercentVO2Max(percent: Double): Double = {
    0.59+0.41*(percent-0.65)/0.35
  }
}
