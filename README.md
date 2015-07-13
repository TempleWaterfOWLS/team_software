Team Software
=========
This repo encapsulates all the code that is meant to be run 
on the main processing unit of The Philadelphia Experiment 
for The TempleWaterfOWLs. At the time of writing, this code has been
tested for Ubuntu 12.04 with ROS Hydro on an HP Pavillion laptop.
<br>
The code is composed of two main components: The ASM and the ROS imaging pipeline.
<br>
# ROS IMAGING PIPELINE
The imaging pipeline has been installed in the catkin_ws of roboboat's
current main processor, the HP Pavillion.
The purpose of this pipeline is to use the 
Bumblebee2 camera to generate pointcloud information.
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
[Stereo Proc Node] (http://wiki.ros.org/stereo_image_proc)
<br>


# ASM
In order to run the barebones code, the two task management functions must be run.
These functions are located in the asm folder, and called
task_asm.py and task_checker.py.





Required Tools:<br>
Python
mitmproxy



#Todo: <br>
* Look in to running stereo_proc as a nodelet, or avoiding the launch from starting a roscore
* Implement python-pcl downsampling of pointcloud