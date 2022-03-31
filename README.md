# pa_gcs_data
Packages needed
1) mavros
2) keyboard (https://github.com/lrse/ros-keyboard)


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


To Run
Follow the instructions on https://ardupilot.org/dev/docs/ros-sitl.html
You shoud have an edited version of apm.launch in ~/catkin_was/launch
1) Terminal 1

        $ cd ~/ardupilot
        $ sim_vehicle.py -v ArduCopter --map --console -L SW
        
2) Terminal 2

        $ roscd
        $ cd ..
        $ roscd launch
        $ roslaunch apm.launch

3) Terminal 3

        $ roscd
        $ cd ..
        $ rosrun keyboard keyboard

4) Terminal 4

        $ roscd
        $ cd ..
        $ rosrun pa_gcs_data FCU_monitor.py
