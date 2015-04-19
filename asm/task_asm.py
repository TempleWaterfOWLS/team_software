'''
Task ASM -> Moves between Tasks
Subscribes to: Complete msg from Task Checker
Publishes: Task Info (CurrentTask)
If current task is complete, change the task
'''

import rospy
from team_software.msg import CurrentTask
from team_software.msg import Complete

# Global break var for switching tasks
old_complete = False
# Global task index for finding task 
task_index = 0

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
    # Current Task Storage
    dum_var = 0
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
