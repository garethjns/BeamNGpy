from time import sleep
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import Advanced_IMU

# Executing this file will perform various tests on all available functionality relating to the advanced IMU sensor.
# It is provided to give examples on how to use all advanced IMU sensor functions currently available in beamngpy.

if __name__ == '__main__':
    set_up_simple_logging()

    # Start up the simulator.
    bng = BeamNGpy('localhost', 64256)
    bng.open(launch=True)
    vehicle = Vehicle('ego_vehicle', model='etki', licence='PYTHON', color='Red')                           # Create a vehicle.
    scenario = Scenario('smallgrid', 'advanced_IMU_test', description='Testing the advanced IMU sensor')    # Create a scenario.
    scenario.add_vehicle(vehicle)                                                                           # Add the vehicle to the scenario.
    scenario.make(bng)
    bng.set_deterministic()
    bng.set_steps_per_second(60)                                                                            # Set simulator to 60hz temporal resolution
    bng.load_scenario(scenario)
    bng.hide_hud()
    bng.start_scenario()

    print("Advanced IMU test start.")

    # Create a default advanced IMU sensor.
    IMU1 = Advanced_IMU('advancedIMU1', bng, vehicle)

    # Test the automatic polling functionality of the advanced IMU sensor, to make sure we retrieve the point cloud data via shared memory.
    sleep(2)
    sensor_readings = IMU1.poll()
    print("advanced IMU readings (automatic polling): ", sensor_readings)

    # Test the ad-hoc polling functionality of the advanced IMU sensor. We send an ad-hoc request to poll the sensor, then wait for it to return.
    sleep(1)
    print("Ad-hoc poll request test.")
    request_id = IMU1.send_ad_hoc_poll_request()                                                  # send an ad-hoc polling request to the simulator.
    print("Ad-hoc poll requests sent. Unique request Id number: ", request_id)
    sleep(3)
    print("Is ad-hoc request complete? ", IMU1.is_ad_hoc_poll_request_ready(request_id)['data'])  # Ensure that the data has been processed before collecting.
    sensor_readings_ad_hoc = IMU1.collect_ad_hoc_poll_request(request_id)                         # Collect the data now that it has been computed.
    print("advanced IMU readings (ad-hoc polling): ", sensor_readings_ad_hoc)
    IMU1.remove()
    print("advanced IMU sensor removed.")

    # Create an advanced IMU sensor which has a negative requested update rate, and ensure that no readings are computed from it.
    IMU2 = Advanced_IMU('advancedIMU2', bng, vehicle, gfx_update_time=-1.0)
    print("Testing an advanced IMU sensor with a negative requested update time...")
    sleep(2)
    sensor_readings = IMU2.poll()
    print("advanced IMU readings (should be zeros): ", sensor_readings)
    IMU2.remove()

    # Recreate the first advanced IMU sensor.
    IMU1 = Advanced_IMU('advancedIMU1', bng, vehicle)

    # Test that the property getter function return the correct data which was set.
    sleep(1)
    print("Property getter test.  The displayed values should be the values which were set during the creation of the advanced IMU sensor.")
    print("Sensor Name: ", IMU1.name)

    # Test changing the visibility of the sensor.
    print("Test visibility mode.  Advanced IMU visibility should cycle between on and off 3 times, staying at each for 1 second.")
    sleep(1)
    IMU1.set_is_visualised(False)
    sleep(1)
    IMU1.set_is_visualised(True)
    sleep(1)
    IMU1.set_is_visualised(False)
    sleep(1)
    IMU1.set_is_visualised(True)
    sleep(1)
    IMU1.set_is_visualised(False)
    sleep(1)
    IMU1.set_is_visualised(True)

    IMU1.remove()

    sleep(3)
    print("advanced IMU test complete.")

    # Close the simulation.
    bng.close()
