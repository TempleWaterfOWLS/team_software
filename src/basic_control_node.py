#!/usr/bin/env python
'''
 Node to interface motor controllers to ROS
 Looks for motor power and motor node number from ROS 
 Outputs the motor response information to ROS
'''

import rospy
from team_software.msg import MotorPower
from team_software.msg import RandTheta
from team_software.msg import Stop

# Global stopvar
fuck_the_police = False

def power_level(data,motor_power):
  '''
  Function to send power levels to motor 
  '''

  if data.theta < 0: 
    motor_power.power1= 0.1
    motor_power.power2=-0.1
  elif data.theta > 0:
    motor_power.power1 = -0.1
    motor_power.power2 =  0.1
  elif data.theta == 0:
    motor_power.power1 = 0.1
    motor_power.power2 = 0.1
  else: 
    motor_power.power1 = 0
    motor_power.power2 = 0

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
  pub = rospy.Publisher('motor_power', MotorPower, queue_size=10)
  rospy.init_node('control_node')
  rate = rospy.Rate(10)
  motor_power=MotorPower()

  motor_power.power1=0.0
  motor_power.power2=0.0

  # spins at rate and puts the motors response on ROS
  # send true on Stop topic to stop motors
  while not rospy.is_shutdown():
    if (fuck_the_police):
        motor_power.power1=0.0
        motor_power.power2=0.0
        pub.publish(motor_power)
    else:
      pub.publish(motor_power)
    rospy.Subscriber("RandTheta", RandTheta, power_level, motor_power)
    rospy.Subscriber("Stop", Stop, check_stop)
    rate.sleep()


if __name__ == '__main__':
  try: 
    motor_node()
  except rospy.ROSInterruptException:
    pass
