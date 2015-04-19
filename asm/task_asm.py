'''
Task ASM -> Moves between Tasks
Subscribes to: Complete msg from Task Checker
Publishes: Task Info (CurrentTask)
If current task is complete, change the task
'''
import threading
import rospy
import subprocess
import take_frame as tf
import cv2
import os

from team_software.msg import CurrentTask
from team_software.msg import Complete

# Global break var for switching tasks
old_complete = False
# Global task index for finding task 
task_index = 0

def hbeat():
    subprocess.call(['python','heartbeat.py'])      

def take_img():
    counter = 0
    while 1:
        #try:
            frame = tf.take_frame()
            fname = "./image_dump/" + str(counter) + '.jpg'
            while(os.path.isfile(fname)):
                counter += 1
                fname = "./image_dump/" + str(counter) + '.jpg'
            cv2.imwrite("./image_dump/"+str(counter) + '.jpg' ,frame)
            counter += 1
        #except:
        #    pass

def Complete_Callback(data,task_array):
    global old_complete
    global task_index
    # If the complete signal hasn't changed, then don't change task
    if old_complete == data.complete:
        task_index = task_index
    else:
        if (data.complete != False):
            old_complete = data.complete
            task_index = task_index+1
            if (task_index >= len(task_array)): task_index = len(task_array) - 1
        else:
            old_complete = data.complete

def task_selector():
    # Start heartbeat
    t = threading.Thread(target=hbeat)
    t.setDaemon(True)
    t.start()
    # Start captures
    d = threading.Thread(target=take_img)
    d.setDaemon(True)
    d.start()
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
