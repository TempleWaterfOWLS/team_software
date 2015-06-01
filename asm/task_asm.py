'''
Task ASM -> Moves between Tasks
Subscribes to: Complete msg from Task Checker
Publishes: Task Info (CurrentTask)
If current task is complete, change the task
'''

# Heartbeat runs on independent thread
import threading
# ROS signaling 
import rospy
# Used to call individual tasks via bash
import subprocess
# Used to take and save images
import take_frame as tf
import cv2
import os

# ROS Messages
from team_software.msg import CurrentTask
from team_software.msg import Complete

# Global break var for switching tasks
old_complete = False
# Global task index for finding task 
# Considering an initial optional user input to set task
task_index = 0

# Call heartbeat code (running on separate thread)
def hbeat():
    subprocess.call(['python','heartbeat.py'])      

# Save image data and disparity (running on separate thread)
def take_img():
    while 1:
         tf.get_data()

def Complete_Callback(data,task_array):
    '''
    Function to deal with a completed task (activates when ROS msg 'Complete' changes)
    '''
    global old_complete
    global task_index
    # If the complete signal hasn't changed, then don't change task
    if old_complete == data.complete:
        task_index = task_index
    else:
        # If complete is true, change the task 
        if (data.complete):
            old_complete = data.complete
            task_index = task_index+1
            # Make sure you don't go past the max length of task array
            if (task_index >= len(task_array)): task_index = len(task_array) - 1
        else:
            old_complete = data.complete

def task_selector():
    ''' 
    Main function for ASM, starts normal operation
    Initializes heartbeat
    Starts data collection
    Manages processes
    '''
    ### Thread Initializations ###

    ### Heartbeat
    t = threading.Thread(target=hbeat)
    t.setDaemon(True)
    t.start()
    ### Frame Capture
    d = threading.Thread(target=take_img)
    d.setDaemon(True)
    d.start()

    ### Process Management Section ###

    # Current Task Storage
    task_array = ["speed", "obstacle", "docking","pinger","quad", "return"]
    # Ros publisher stuff
    pub = rospy.Publisher('CurrentTask', CurrentTask, queue_size=10)
    rospy.init_node('taskasm')
    rate = rospy.Rate(10)
    curr_task=CurrentTask()
    while not rospy.is_shutdown():
        # Get current task
        curr_task.currentTask = task_array[task_index]
        # Publish current task
        pub.publish(curr_task)
        # Listen for the break signal
        rospy.Subscriber("Complete", Complete, Complete_Callback, task_array)
        rate.sleep()

if __name__ == '__main__':
    try: 
        task_selector()
    except rospy.ROSInterruptException:
        pass
