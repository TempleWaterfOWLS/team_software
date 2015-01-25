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



# To do: fix handlers, make input better defined
def main():
    ''' 
    Parse command line args and determine state
    ''' 
    try: 
        cpp_file = argv[1]
        stdin_args = argv[2].split()
    # Handle no args
    except:
        cpp_file = None
        stdin_args = None
    # Call Cpp file
    if cpp_file != None:
        cpp_file = "./" + cpp_file
        cpp_file = [cpp_file]
        call(cpp_file + stdin_args)

    else:
        print "No Cpp file"
    print "Things are happening out of order"

# Boiler plate code
if __name__ == '__main__':
    main()
