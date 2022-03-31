#!/usr/bin/env python

#This monitors the flight status of a suite of the FCU.

from ssl import ALERT_DESCRIPTION_UNSUPPORTED_EXTENSION
import sys
import rospy
import math
import csv
import os

from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from keyboard.msg import Key
from std_msgs.msg import Bool

class GetData():
    
    def __init__(self):
        self.gps = rospy.Subscriber('/mavros/global_position/global', NavSatFix, self.GPS_callback)
        self.imu = rospy.Subscriber('/mavros/imu/data', Imu, self.IMU_callback)
        self.lidar = rospy.Subscriber('/mavros/global_position/rel_alt', Float64, self.Alt_callback)
        self.keyboard_sub = rospy.Subscriber('/keyboard/keydown', Key, self.get_key)
        self.gps_lat = 0
        self.gps_long = 0
        self.yaw = 0
        self.altitude = 0
        self.key_code = -1
        self.mainloop()
        
    def GPS_callback(self, msg):
        self.gps_lat = msg.latitude
        self.gps_long = msg.longitude

    def IMU_callback(self, msg):
        x = msg.orientation.x
        y = msg.orientation.y
        z = msg.orientation.z
        w = msg.orientation.w
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)

        self.yaw = math.atan2(t3, t4)

    def Alt_callback(self, msg):
        self.altitude = msg.data

    def get_key(self, msg):
        self.key_code = msg.code

    def CSV_writer(self):
        dest_dir = '/home/ezra/pa_data/'
        file_path = os.path.join(dest_dir, 'target_data.csv')
        with open(file_path, 'wb') as csvfile:
            names = ['yaw_angle', 'gps_latitude', 'gps_longitude', 'altitude']
            dataWriter = csv.DictWriter(csvfile, fieldnames=names)
            dataWriter.writeheader()
            dataWriter.writerow({'yaw_angle': self.yaw, 'gps_latitude': self.gps_lat, 'gps_longitude': self.gps_long, 'altitude': self.altitude})
        
    def mainloop(self):
        # Set the rate of this loop
        rate = rospy.Rate(5)
        # While ROS is still running
        while not rospy.is_shutdown():
            # Check if any key has been pressed
            if self.key_code == Key.KEY_a:
                # "a" key was pressed
                print("a key was pressed!")
                rospy.loginfo("Altitude: %f" %self.altitude)
                rospy.loginfo("Latitude: %f" %self.gps_lat)
                rospy.loginfo("Longitude: %f" %self.gps_long)
                rospy.loginfo("Yaw Angle: %f" %self.yaw)
                self.CSV_writer()

            # Reset the code
            if self.key_code != -1:
                self.key_code = -1

            # Sleep for the remainder of the loop
            rate.sleep()
      
if __name__ == '__main__':
    rospy.init_node('get_data_node')
    try:
        ktp = GetData()
    except rospy.ROSInterruptException:
        pass