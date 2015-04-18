import cv2
import numpy as np


def main():
    # Iterate over lines in out.pts
    w,h = 320,240
    img = np.zeros((h,w,3),dtype=np.uint8)
    img[:] = [0,0,0]

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
