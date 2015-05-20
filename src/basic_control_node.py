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

class motor_control ():
  def __init__(self):
    self.motor_rpm=MotorRPM()
    self.motor_rpm.rpm0=0.0
    self.motor_rpm.rpm1=0.0
    self.rpm_scalar=200
    self.pub = rospy.Publisher('motor_rpm', MotorRPM, queue_size=10)

def set_rpm(data,motors):
  '''
  Function to send rpm levels to motor 
  Angles are increase CCW
  Motor0 is on left. Motor1 is on right
  '''
  
  if data.theta <= 90 and data.theta >= 0:
    motors.motor_rpm.rpm0 = motors.rpm_scalar*(-2*data.r/90*data.theta+data.r)
    motors.motor_rpm.rpm1 = motors.rpm_scalar*data.r
    
  elif data.theta <=360 and data.theta > 270:
    motors.motor_rpm.rpm0 = motors.rpm_scalar*data.r
    motors.motor_rpm.rpm1 = motors.rpm_scalar*(2*data.r/90*data.theta-7*data.r)   
    
  elif data.theta <= 180 and data.theta > 90:
    motors.motor_rpm.rpm0 = -motors.rpm_scalar*data.r
    motors.motor_rpm.rpm1 = motors.rpm_scalar*(-2*data.r/90*data.theta+3*data.r)
    
  elif data.theta <= 270 and data.theta > 180:
    motors.motor_rpm.rpm0 = motors.rpm_scalar*(2*data.r/90*data.theta-5*data.r)
    motors.motor_rpm.rpm1 = -motors.rpm_scalar*data.r
  
  elif data.theta < 0:
      motors.motor_rpm.rpm0= 0
      motors.motor_rpm.rpm1= 0
  else:
    data.theta=data.theta-360
    set_rpm(data,motors)
    
 # motors.pub(motors.motor_rpm)  
'''
  if data.theta < 0: 
    motor_rpm.rpm0= rpm_scalar*data.r
    motor_rpm.rpm1= -rpm_scalar*data.r
  elif data.theta > 0:
    motor_rpm.rpm0 = -rpm_scalar*data.r
    motor_rpm.rpm1 =  rpm_scalar*data.r
  elif data.theta == 0:
    motor_rpm.rpm0 = rpm_scalar*data.r
    motor_rpm.rpm1 = rpm_scalar*data.r
  else: 
    motor_rpm.rpm0 = 0
    motor_rpm.rpm1 = 0
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
  motors=motor_control()
  rospy.init_node('control_node')
  rate = rospy.Rate(10)
 
  # spins at rate and puts the motors response on ROS
  # send true on Stop topic to stop motors
  while not rospy.is_shutdown():
    if (fuck_the_police):
        motors.motor_rpm.rpm0=0.0
        motors.motor_rpm.rpm1=0.0
        motors.pub.publish(motors.motor_rpm)
    else:
       motors. pub.publish(motors.motor_rpm)
    rospy.Subscriber("RandTheta", RandTheta, set_rpm, motors)
    rospy.Subscriber("Stop", Stop, check_stop)
    rate.sleep()


if __name__ == '__main__':
  try: 
    motor_node()
  except rospy.ROSInterruptException:
    pass
