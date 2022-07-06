from time import sleep
from beamngpy import BeamNGpy, Scenario, Vehicle, setup_logging
from beamngpy.ultrasonic import Ultrasonic

# Executing this file will perform various tests on all available functionality relating to the ultrasonic sensor.
# It is provided to give examples on how to use all ultrasonic sensor functions currently available in beamngpy. 

setup_logging()

# Start up the simulator.
beamng = BeamNGpy('localhost', 64256)
bng = beamng.open(launch=True)

vehicle = Vehicle('ego_vehicle', model='etki', licence='PYTHON', color='Red')                       # Create a vehicle.
scenario = Scenario('smallgrid', 'ultrasonic_test', description='Testing the ultrasonic sensor')    # Create a scenario.
scenario.add_vehicle(vehicle, pos=(0, 0, 0), rot=(0, 0, 0))                                         # Add the vehicle to the scenario.
scenario.make(bng)

bng.set_deterministic()
bng.set_steps_per_second(60)        # Set simulator to 60hz temporal resolution

bng.load_scenario(scenario)
bng.hide_hud()
bng.start_scenario()

print("Ultrasonic test start.")

# Create a default ultrasonic sensor.
ultrasonic1 = Ultrasonic('ultrasonic1', bng, vehicle)

# Test the automatic polling functionality of the ultrasonic sensor, to make sure we retrieve the readings.
sleep(2)
sensor_readings = ultrasonic1.poll()
print("Ultrasonic readings (automatic polling): ", sensor_readings)

# Test the ad-hoc polling functionality of the ultrasonic sensor. We send an ad-hoc request to poll the sensor, then wait for it to return.
sleep(1)
print("Ad-hoc poll request test.")
request_id = ultrasonic1.send_ad_hoc_poll_request()                                                     # send an ad-hoc polling request to the simulator.
print("Ad-hoc poll requests sent. Unique request Id number: ", request_id)
sleep(3)
print("Is ad-hoc request complete? ", ultrasonic1.is_ad_hoc_poll_request_ready(request_id)['data'])     # Ensure that the data has been processed before collecting.
sensor_readings_ad_hoc = ultrasonic1.collect_ad_hoc_poll_request(request_id)                            # Collect the data now that it has been computed.
print("Ultrasonic readings (ad-hoc polling): ", sensor_readings_ad_hoc)
ultrasonic1.remove()
print("Ultrasonic sensor removed.")

# Create an ultrasonic sensor which has a negative requested update rate, and ensure that no readings are computed from it.
ultrasonic2 = Ultrasonic('ultrasonic2', bng, vehicle, requested_update_time=-1.0)
print("Testing an ultrasonic sensor with a negative requested update time...")
sleep(2)
sensor_readings = ultrasonic2.poll()
print("Ultrasonic readings (should be zeros): ", sensor_readings)
ultrasonic2.remove()

# Recreate the first ultrasonic sensor.
ultrasonic1 = Ultrasonic('ultrasonic1', bng, vehicle)

# Test that the property getter function return the correct data which was set.
sleep(1)
print("Property getter test.  The displayed values should be the values which were set during the creation of the ultrasonic sensors.")
print("Sensor Name: ", ultrasonic1.name)
print("Position: ", ultrasonic1.get_position())
print("Direction: ", ultrasonic1.get_direction())
print("Requested update time: ", ultrasonic1.get_requested_update_time())
print("Priority: ", ultrasonic1.get_update_priority())
print("Max Pending Requests: ", ultrasonic1.get_max_pending_requests())
print("Is Visualised [Flag]: ", ultrasonic1.get_is_visualised())

# Test that we can set the sensor core properties in the simulator from beamngpy.
sleep(1)
print("Property setter test.  The displayed property values should be different from the previous values.")
ultrasonic1.set_requested_update_time(0.3)
print("Newly-set Requested Update Time: ", ultrasonic1.get_requested_update_time())
ultrasonic1.set_update_priority(0.5)
print("Newly-set Priority: ", ultrasonic1.get_update_priority())
ultrasonic1.set_max_pending_requests(5)
print("Newly-set Max Pending Requests: ", ultrasonic1.get_max_pending_requests())

# Test changing the visibility of the sensor.
print("Test visibility mode.  Ultrasonic visibility should cycle between on and off 3 times, staying at each for 1 second.")
sleep(1)
ultrasonic1.set_is_visualised(False)
sleep(1)
ultrasonic1.set_is_visualised(True)
sleep(1)
ultrasonic1.set_is_visualised(False)
sleep(1)
ultrasonic1.set_is_visualised(True)
sleep(1)
ultrasonic1.set_is_visualised(False)
sleep(1)
ultrasonic1.set_is_visualised(True)

ultrasonic1.remove()

sleep(3)
print("Ultrasonic test complete.")

# Close the simulation.
beamng.close()
