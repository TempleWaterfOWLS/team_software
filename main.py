'''
Main python code for team software. Calls all other functions required for operation. 
Ideally, it will contain: 
-An Algorithmic State Machine (ASM) to determine current task
-Function calls to appropriate tasks
-Ability to pass data from sensors to different modules

Written by team software (Zack Smith & Taylor Million) 1/25/15

Todo: Everything
Usage: Not yet determined
''' 

# Imports 
from subprocess import call
from sys import argv
import cv2
import colordetection as cd

# To do: fix handlers, make input better defined, make more efficient
def main():
    ''' 
    Parse command line args and determine state
    ''' 
    # Default parameters
    stdin_args = ''
    cpp_file = "triclops/src/examples/common/stereoto3dpoints/stereoto3dpoints"
    reconstruct_file = "./triclops/src/examples/common/stereoto3dpoints/reconstruction.py"
    # Parse for inputs
    if len(argv) == 2:
        cpp_file = argv[1]
    elif len(argv) == 3:
        cpp_file = argv[1]
        stdin_args = argv[2]
    # Try to call C++ file
    try: 
        cpp_file = "./" + cpp_file
        cpp_file = [cpp_file]
        call(cpp_file + stdin_args.split())
        call([reconstruct_file])
    # Handle exception
    except:
        print 'Except block'
        cpp_file = None
        stdin_args = None
    # After triclops stuff has been done, perform cv operations
    ### Operations: Color Detection, Contour Finding, logic? ###
    cd.color_detect(['rectified.pgm'])


# Boiler plate code
if __name__ == '__main__':
    main()
