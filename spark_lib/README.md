# Analyze RunningAhead logs using Spark

Two types of logs
1. By activity, all the fields contributing to activity summary.
Mostly used columns:
- Date
- TimeOfDay
- Type
- SubType
- Distance
- DistanceUnit
- Duration
- AvgHR
- MaxHR
2. By interval, stats for each interval. This log is very helpful for evaluating the performance of a specific type
