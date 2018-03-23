from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

# to calculate distance
def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def armingAndTakeOff(targetAltitude):
    print("Basic pre arm check")
    while not myVehicle.is_armable:
        print("Waiting myVehicle ready....")
        time.sleep(1)

    # arming
    myVehicle.mode = VehicleMode("GUIDED")
    myVehicle.armed = True

    #confirm arming
    while not myVehicle.armed:
        print("Waiting for arming..")
        time.sleep(1)

    # takeoff to spesific altitude
    myVehicle.simple_takeoff(targetAltitude)

    currentAltitude = 0
    while currentAltitude <= targetAltitude*0.95:
        currentAltitude = myVehicle.location.global_relative_frame.alt
        print("Current Altitude : %s" ) % currentAltitude
        time.sleep(1)
    print ("Current Altitude has reached %s" )% targetAltitude

# create vehicle object
sitl_ip = 'udp:127.0.0.1:14551'
myVehicle = connect(sitl_ip, wait_ready=True)

#call the function to arming and takeoff
armingAndTakeOff(10) #with the altitude

#define point coordinate
point1 = LocationGlobalRelative(-6.971506, 107.629066, 35)
point2 = LocationGlobalRelative(-6.972549,	107.631860, 50)
point3 = LocationGlobalRelative(-6.975881, 107.632215, 20)

# set speed vehicle unit is m.s
airSpeed = 30
print ("Set airspeed %d" )% airSpeed
myVehicle.airspeed = airSpeed #set airspeed

# define first coordinate
point1 = LocationGlobalRelative(-6.9715063, 107.6290657, 35)

print("Go to point 1")
myVehicle.simple_goto(point1)
# sleep so we can see the change in map
finished = False
prevLocation = None

while not finished:
    print("waiting...")
    currentGlobalRelative = myVehicle.location.global_relative_frame
    distancePoint1 = get_distance_metres(point1, currentGlobalRelative)
    distancePoint2 = get_distance_metres(point2, currentGlobalRelative)
    distancePoint3 = get_distance_metres(point3, currentGlobalRelative)
    print("distance point 1 : %f") % distancePoint1
    print("distance point 2 : %f") % distancePoint2
    print("distance point 3 : %f") % distancePoint3

    if distancePoint1 < 5:
        # go to waypoint 2
        print("go to point 2")
        myVehicle.simple_goto(point2)
    elif distancePoint2 < 5:
        # go to waypoint 3
        print("go to point 3")
        myVehicle.simple_goto(point3)
    elif distancePoint3 < 5:
        # finish return to home
        finished = True
    else:
        print("On the way to way point ")

    print "Current Location: %s" % currentGlobalRelative

    time.sleep(1)

#when finished
myVehicle.mode = VehicleMode("RTL")

# Close vehicle object
print("Close vehicle")
myVehicle.close()





