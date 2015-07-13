'''
Function written to fuck with point cloud data

'''


import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from time import strftime 
from pprint import pprint
import numpy as np
import sys
sys.path.insert(0,'./python-pcl')
import pcl

global truevar 

def callback(data):
    fmt = _get_struct_fmt(data)
    points = np.array()
    offset = 0
    global truevar
    if not truevar:
        for i in xrange(data.width*data.height):
            p = struct.unpack_from(fmt,data.data,offset)
            offset += data.point_step
            points.append(p)
        print points[0]
        gen = pc2.read_points(data, skip_nans=True,field_names=("x","y","z"))
        #print gen
        '''
        l = dir(data)
        #pprint (l)
        d = dir(data.data)
        #print 'HEADER:'
        #print data.header
        #print 'FIELDS:'
        #print data.fields
        #print 'SERIALIZE'
        # print data.serialize
        print 'DESERIALIZE'
        #print data.deserialize
        '''
        print 'Done!'
        p = pcl.PointCloud()
        p.from_array(points)
        fil = p.make_voxel_grid_filter()
        fil.set_leaf_size(0.1,0.1,0.1)
        fil.filter().to_file("yolo.pcd")
        
    truevar = True

def find_cloud():
    global truevar
    truevar = False
    ### Do PCL Stuff
    p = pcl.PointCloud()
    p.from_file("1436300576827528.pcd")
    fil = p.make_voxel_grid_filter()
    fil.set_leaf_size(0.1,0.1,0.1)
    fil.filter().to_file("yolo.pcd")
    ### Do ROS Stuff
    rospy.init_node('pcl_node')
    rate = rospy.Rate(10)
    print 'starting'
    while not rospy.is_shutdown():
        #PCL Subscriber
        rospy.Subscriber("/stereo_camera/points2", PointCloud2, callback)
        rate.sleep()

if __name__ == '__main__':
    find_cloud()
