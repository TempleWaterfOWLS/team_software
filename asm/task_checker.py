'''
Task Checker -> Executes Different Tasks
Subscribes to: 
-Task Info (CurrentTask) from task_asm.py
-Complete Signals (from different task nodes -> Publish node name, check if active task)

Publishes: 
-Complete (task_asm.py subscribes)
-Kill Command (stops current task)
'''

### ROS Imports
import rospy
# Subscribing
from team_software.msg import CurrentTask
from team_software.msg import SuicideTask
# Publishing
from team_software.msg import Complete
from team_software.msg import TaskStop
### Process Management Imports
import subprocess
import os
import signal
import time

# Global break var for switching tasks
old_complete = False
# Global task index for finding task 
task_index = 0
# Global task var
curr_task = "none"
# Global pid var for current task
process_id = None

def CurrentTask_Callback(data,complete_msg):
    '''
    Function that gets called when currentTask is published
    simply grabs new task and writes it in to curr_task
    '''
    course = ['courseA','courseB','openTest']; IP = '192.168.0.106'
    active_course=course[0]
    complete_msg.complete = False
    global curr_task; global process_id; 
    # If new task, start up new function, and kill old one
    if (curr_task != data.currentTask):
        # Kill old process
        if (process_id != None):
            os.kill(process_id, signal.SIGKILL)
        # Update current task
        curr_task = data.currentTask
        # Run new task
        pro = subprocess.Popen(['python',curr_task+".py",IP,active_course])
        process_id = pro.pid
    # Else, the current task is still running, so nothing must be done
    else:
        pass
def SuicideTask_Callback(data,complete_msg):
    '''
    Function that gets called when a task wants to be killed
    '''
    # If task is suicidal, clear data.suicide, set complete true
    # By publishing task as complete, the current task will be culled
    if (data.suicidetask):
        data.suicidetask = False
        complete_msg.complete = True
    

def task_executor():
    ''' 
    Main function which maintains current task and terminates running code
    '''
    # ROS publisher stuff
    complete_pub = rospy.Publisher('Complete', Complete, queue_size=10)
    rospy.init_node('taskcheck')
    rate = rospy.Rate(10)
    # Initialize messages
    complete_msg = Complete()
    complete_msg.complete = False 
    # ROS main loop
    while not rospy.is_shutdown():
        # Publish Status
        complete_pub.publish(complete_msg)
        # Grab messages that we subscribe to
        rospy.Subscriber("CurrentTask", CurrentTask, CurrentTask_Callback,complete_msg)
        rospy.Subscriber("SuicideTask", SuicideTask, SuicideTask_Callback,complete_msg)
        # Sleep 
        rate.sleep()

if __name__ == '__main__':
    try: 
        task_executor()
    except rospy.ROSInterruptException:
        pass
