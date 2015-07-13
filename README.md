Team Software
=========
This repo encapsulates all the code that is meant to be run 
on the main processing unit of The Philadelphia Experiment 
for The TempleWaterfOWLs. At the time of writing, this code has been
tested for Ubuntu 12.04 with ROS Hydro on an HP Pavillion laptop.
The code is composed of two main components: The ASM and the ROS imaging pipeline.
<br>
# ROS Imaging Pipeline
The imaging pipeline has been installed on the roboboat's
current main processor, the HP Pavillion. It uses the camera1394stereo driver, 
which is located in the catkin_ws of the main processor.
The purpose of this pipeline is to use the 
Bumblebee2 camera to generate pointcloud information.

* This PointCloud information should then be further processed by python pcl 
and then used in the ROS Navigation pipeline, or a custom navigation 
algorithm.*

To run this pipeline, you should type the following commands:
```
roslaunch camera1394stereo stereo_camera.launch
```

In a new shell, type:

```
ROS_NAMESPACE=stereo_camera rosrun stereo_image_proc stereo_image_proc  
```

This will run the driver for the bumblebee2 camera and begin stereo processing on 
incoming images. To view these images, type:

```
rosrun image_view stereo_view stereo:=/stereo_camera image:=image_rect_color
```

To see all the topics that these nodes are publishing, type rostopic list. 
For more information on the image pipeline, check out these docs: <br>
[Stereo Calibration] (http://wiki.ros.org/camera_calibration/Tutorials/StereoCalibration)
<br>
[Stereo Image Proc Node] (http://wiki.ros.org/stereo_image_proc)
<br>


# ASM
In order to run the barebones code, the two task management functions must be run.
These functions are located in the asm folder, and called
task_asm.py and task_checker.py. <br><br>
The task_asm.py (hereafter referred to as 'task asm') file maintains a 
queue of the tasks to be completed, and publishes them on the ROS 
message, 'CurrentTask'. It also subscribes to the ROS 'Complete' message,
and will jump to the next task when this 'Complete' message is received.
Other than maintaining this task queue, the task asm also initializes the 
"heartbeat" requirement of the challenge. It also has the ability to capture
and save images to the hard drive for later analytics, which is not currently
up to date and is thus commented out. The task asm runs these algorithms in
separate threads.
<br>
The task checker module will execute the current task and terminate any 
task which meets its end conditions. It does this by subscribing to the 
ROS 'CurrentTask' message, and running a file which is named after
the current task (e.g, if the CurrentTask message is 'speed', the task
checker module will run 'speed.py'). It kills these modules by subscribing
to their published ROS message, 'SuicideTask'. The checker also publishes 
the ROS 'Complete' message, so that the queue can be updated by the task asm.
For more information on these files, and the individual module files,
read the source code located in the asm directory. 

# Networking
<br>
# Development
<br>
#Required Tools:<br>
* Python
* ROS
* mitmproxy



#Todo: <br>
* Look in to running stereo_proc as a nodelet, or avoiding the launch from starting a roscore
* Implement python-pcl downsampling of pointcloud
* Introduce [ROS Navigation] (http://wiki.ros.org/navigation) or a custom algorithm for navigation
