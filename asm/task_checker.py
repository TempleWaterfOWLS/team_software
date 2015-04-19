'''
Task Checker -> Executes Different Tasks
Subscribes to: 
-Task Info (CurrentTask) from task_asm.py
-Complete Signals (from different task nodes -> Publish node name, check if active task)

Publishes: 
-Complete (ASM.py subscribes)
-Kill Command (stops current task)

'''

import rospy
# Subscribing
from team_software.msg import CurrentTask
from team_software.msg import SuicideTask
# Publishing
from team_software.msg import Complete
from team_software.msg import TaskStop

# Subprocess management import
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
    complete_msg.complete = False
    global curr_task; global process_id; 
    # If new task, start up new function, and kill old one
    if (curr_task != data.currentTask):
        # Kill last process
        if (process_id != None):
            os.kill(process_id, signal.SIGKILL)
        curr_task = data.currentTask
        # Run new task
        pro = subprocess.Popen(['python',curr_task+".py"])
        process_id = pro.pid

def SuicideTask_Callback(data,complete_msg):
    '''
    Function that gets called when a task wants to be killed
    '''
    # If task is suicidal, clear data.suicide, set complete true
    # In current task, set complete back to false
    # Just publish complete. This will force task forward and delete current
    if (data.suicidetask):
        data.suicidetask = False
        complete_msg.complete = True
    

def task_executor():
    ''' 
    Main function which maintains current task and terminates running code
    '''
    # Ros publisher stuff
    complete_pub = rospy.Publisher('Complete', Complete, queue_size=10)
    taskstop_pub = rospy.Publisher('TaskStop', TaskStop, queue_size=10)
    rospy.init_node('taskcheck')
    rate = rospy.Rate(10)
    complete_msg = Complete()
    stop_msg = TaskStop()
    complete_msg.complete = False 
    stop_msg.taskstop = "NoNeed"
    while not rospy.is_shutdown():
        # Publish Status
        complete_pub.publish(complete_msg)
        # Publish kill command
        taskstop_pub.publish(stop_msg)
        # Grab current task and any kill signal
        rospy.Subscriber("CurrentTask", CurrentTask, CurrentTask_Callback,complete_msg)
        rospy.Subscriber("SuicideTask", SuicideTask, SuicideTask_Callback,complete_msg)
        rate.sleep()

if __name__ == '__main__':
    try: 
        task_executor()
    except rospy.ROSInterruptException:
        pass
