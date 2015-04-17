#!/usr/bin/env python
'''
 Node to interface motor controllers to ROS
 Looks for motor rpm and motor node number from ROS 
 Outputs the motor response information to ROS
'''

import rospy
from team_software.msg import MotorRPM
from team_software.msg import RandTheta
from team_software.msg import Stop

# Global stopvar
fuck_the_police = False

def set_rpm(data,motor_rpm,rpm_scalar):
  '''
  Function to send rpm levels to motor 
  '''

  if data.theta < 0: 
    motor_rpm.rpm1= 1000
    motor_rpm.rpm2=-1000
  elif data.theta > 0:
    motor_rpm.rpm1 = -1000
    motor_rpm.rpm2 =  1000
  elif data.theta == 0:
    motor_rpm.rpm1 = 1000
    motor_rpm.rpm2 = 1000
  else: 
    motor_rpm.rpm1 = 0
    motor_rpm.rpm2 = 0

def polar_to_cart():
  '''
  Function to take an R and Theta and convert it to X and
  '''
    
def check_stop(data):
  # Set global for modify purposes
  global fuck_the_police
  fuck_the_police = data.stop
  '''
  if (data.stop == 0.0):
    fuck_the_police = False
  else: 
    fuck_the_police = True
  '''  
def motor_node():
  '''
  Top level function to handle connection of motors with ROS
  '''
  pub = rospy.Publisher('motor_rpm', MotorRPM, queue_size=10)
  rospy.init_node('control_node')
  rate = rospy.Rate(10)
  motor_rpm=MotorRPM()

  motor_rpm.rpm1=0.0
  motor_rpm.rpm2=0.0
  rpm_scalar=1
  
  # spins at rate and puts the motors response on ROS
  # send true on Stop topic to stop motors
  while not rospy.is_shutdown():
    if (fuck_the_police):
        motor_rpm.rpm1=0.0
        motor_rpm.rpm2=0.0
        pub.publish(motor_rpm)
    else:
      pub.publish(motor_rpm)
    rospy.Subscriber("RandTheta", RandTheta, set_rpm, motor_rpm, rpm_scalar)
    rospy.Subscriber("Stop", Stop, check_stop)
    rate.sleep()


if __name__ == '__main__':
  try: 
    motor_node()
  except rospy.ROSInterruptException:
    pass
