#!/usr/bin/env python

import cv2
import numpy as np

# Date: 2/9/2015
# Change: Correlating pixel-distance in order to do navigation decision making
# Non optimal search for Z clusters

def main():
    # Define threshold for z distance to trigger detection 
    dist_threshold = 100;
    ''' Non optimal solution start '''
    # Read in whole buffer in to memory 
    # All data is now held in memory (split_file)
    temp_file = open('out.pts', 'r') 
    totaltemp = temp_file.read()
    split_file = totaltemp.split('\n')
    temp_buffer = []
    # Iterate over all data (split_file) 
    # 1st pass check for less than Z, "tag it" --> Write to secondary buffer            
    for rows in split_file:
        # format = [x][y][z][r][g][b][y][x]
        row = rows.split()
        try:
            z = float(row[2])
        except:
            continue
        r,g,b = row[3:6]
        # Search for clusters of Z < threshold
        if (z < dist_threshold and z != 0):          
            # Write to secondary buffer
            temp_buffer.append(row)
    # Debug info
    print len(split_file)
    print len(temp_buffer)
    # Cluster parameters
    clusters = []
    curr_cluster = []
    tolerance = 0.01
    
    # 2nd pass through secondary buffer ---> Check for clusters 
    img = cv2.imread('/home/roboboat/repos/team_software/triclops/src/examples/common/stereoto3dpoints/right-rectified.pgm')
    for index,pcl_row in enumerate(temp_buffer):
        lines = pcl_row
        # format = [x][y][z][r][g][b][y][x]
        curr_x = lines[7]; curr_y = lines[6]
        curr_b = int(lines[5]); curr_g = int(lines[4]); curr_r = int(lines[3])
        img[curr_y,curr_x] = [0,0,curr_r]

    cv2.imwrite("cluster.png",img)
    # Cluster search algo = Check adjacent pixels within threshold +- change
    
    # If in cluster, set black else continue with life

    ''' Non optimal solution end '''
    # Rebuild the image
    rebuild_img()

# Function to reconstruct output image in RGB for visualization purposes
def rebuild_img():
    # Image parameters
    w,h = 320,240
    img = np.zeros((h,w,3),dtype=np.uint8)
    img[:] = [0,0,0]
    # Iterate over lines in out.pts
    with open('out.pts','r') as infile:
        for lines in infile:
            lines = lines.split()
            # format = [x][y][z][r][g][b][y][x]
            curr_x = lines[7]; curr_y = lines[6]
            curr_b = int(lines[5]); curr_g = int(lines[4]); curr_r = int(lines[3])
            img[curr_y,curr_x] = [curr_b,curr_g,curr_r]

    cv2.imwrite("yolo.png",img)

if __name__ == '__main__':
    main()
    
