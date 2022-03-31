# PA_GCS_Data

How Code works:
1) Subscribes from following mavros topics (message type)
        - global_position/global (sensor_msgs/NavSatFix)
              Get the Latitude and Longitude
        - global_position/rel_alt (std_msgs/Float64)
              Get the altitude
        - imu/data (sensor_msgs/imu)
              Calculate for the yaw angle

2) Subsribe from the keyboard/keydown topic to check fro key press
3) if key is presses, print the data on terminal and save into csv file
