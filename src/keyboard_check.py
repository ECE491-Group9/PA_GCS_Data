#!/usr/bin/env python
import rospy
from keyboard.msg import Key
from std_msgs.msg import Bool

# Create a class which we will use to take keyboard commands and convert them to an abort message
class KeyboardManager():
  # On node initialization
  def __init__(self):
    # Create the publisher and subscriber
    self.abort_pub = rospy.Publisher('/get_data', Bool, queue_size=1)
    self.keyboard_sub = rospy.Subscriber('/keyboard/keydown', Key, self.get_key, queue_size=1)
    # Create the abort message we are going to be sending
    self.abort = Bool()
    # Create a variable we will use to hold the keyboard code
    self.key_code = -1
    # Call the mainloop of our class
    self.mainloop()

  # Callback for the keyboard sub
  def get_key(self, msg):
    self.key_code = msg.code

  def mainloop(self):
    # Set the rate of this loop
    rate = rospy.Rate(5)
    # While ROS is still running
    while not rospy.is_shutdown():
      # Publish the abort message
      self.abort_pub.publish(self.abort)

      # Check if any key has been pressed
      if self.key_code == Key.KEY_a:
        # "a" key was pressed
        print("a key was pressed!")
        self.abort.data = True

      # Reset the code
      if self.key_code != -1:
        self.key_code = -1

      # Sleep for the remainder of the loop
      rate.sleep()

if __name__ == '__main__':
  rospy.init_node('keyboard_check_node')
  try:
    ktp = KeyboardManager()
  except rospy.ROSInterruptException:
    pass