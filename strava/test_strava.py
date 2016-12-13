from strava import Strava

strava_obj = Strava("/home/predrag/Programs/Running/strava/strava.cfg")
print "Test getAthleteSelf"
ret = strava_obj.getAthleteInfoSelf()
print ret

print "Test getAthlete"
ret = strava_obj.getAthleteInfo(13336453)
print ret

print "Test getClub"
ret = strava_obj.getClub(234023)
print ret
