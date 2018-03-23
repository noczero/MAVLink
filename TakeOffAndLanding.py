from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
# make the vehicle object with the UDP port
sitl_ip = 'udp:127.0.0.1:14551' # this ip in the mavproxy out
myVehicle = connect(sitl_ip,wait_ready=True)

# Steps
# 1. wait until vehicle is arm_able
# 2. then set the mode to guided
# 3. then set the armed to true
# 4. takeoff to the target altitude
# 5. then print "reached target altitude" if the vehicle is achive the estimation attitude

## Precheck section
print("Basic pre-arm checks")
# dont try to arm until the hardware (autopilot) is ready, ensure that it is safe to fly.
# The flight controller will not arm until the vehicle has passed a series of pre-arm checks.

if myVehicle.mode.name == "INITIALISING":
    print "Waiting for vehicle to initialise"
    time.sleep(1)

# waiting for 2D fix
while myVehicle.gps_0.fix_type < 2:
    # about the fix type
    # 0 -1: no fix
    # 2 : 2D fix
    # 3 : 3D fix
    print "Waiting for GPS...:", myVehicle.gps_0.fix_type
    time.sleep(1)

# check again is the vehicle can arm?
while not myVehicle.is_armable:
    print("Final check...")
    time.sleep(1)

## Arming Section
# we start to arming motor
print("Arming Motor")
# copter should arm in GUIDED mode
myVehicle.mode = VehicleMode("GUIDED") # there are several mode in Copter,Plane and Rover : AUTO, GUIDED and RETURN_TO_LUNCH.
myVehicle.armed = True

# confirm vehicle armed before attemping to take off
while not myVehicle.armed:
    print "Waiting for arming..."
    time.sleep(1)


## Take Off section
print("Taking off")
targetAltitude = 15 #
myVehicle.simple_takeoff(targetAltitude) # take off to target altitude in this case is 15 m

## Notification Section
hasReach = False
while not hasReach :
        currentAltitude = myVehicle.location.global_relative_frame.alt
        print("Altitude : %s" ) % currentAltitude
        if myVehicle.location.global_relative_frame.alt >= targetAltitude :
            print("Reached target altitude at %s") % currentAltitude
            hasReach = True
            break
        time.sleep(1)


myVehicle.mode = VehicleMode("RTL") # Landing
myVehicle.close() # close connection





