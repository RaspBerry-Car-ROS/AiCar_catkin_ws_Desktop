#!/usr/bin/env python
import rospy
import tty, termios, sys, os
from teleoperation_publisher.msg import motors_signal


# init :
def publisher():
    rospy.init_node('keyboard_teleop', anonymous=True)
    pub = rospy.Publisher('/motors_topic', motors_signal, queue_size=10)
    # define constants :
    KEY_UP = 65
    KEY_DOWN = 66
    KEY_RIGHT = 67
    KEY_LEFT = 68
    KEY_Q = 81
    KEY_Q2 = 113
    KEY_S = 83
    KEY_S2 = 115
    MOVE_TIME = 0.01

    # define variables :
    speed = 0.0
    rotationalSpeed = 0.0
    keyPress = 0
    linearDirection = 0
    rotationalDirection = 0
    linearSpeed = 0
    rotationalSpeed = 0
    # get char :
    keyPress = " "
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    motor = motors_signal()
    oldKey = 0
    while True:
            
        print(" - AI car manual control \n")
        print("      > Arrows = move robot \n")
        print("      > s = stop \n")
        print("      > q = quit \n")
        rospy.loginfo("motor left :%i  motor right: %i"%(motor.motor_left,motor.motor_right))
        
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        keyPress = ord(ch)
        if keyPress != oldKey:
            os.system('clear')
        # test command :
        if (keyPress == KEY_UP):
            motor.motor_left = 1
            motor.motor_right = 1
            rospy.loginfo("\u2191\u2191\u2191\u2191 forward \u2191\u2191\u2191\u2191")
        elif (keyPress == KEY_DOWN):
            motor.motor_left = -1
            motor.motor_right = -1
            rospy.loginfo ("\u2193\u2193\u2193\u2193 backward \u2193\u2193\u2193\u2193")
        elif (keyPress == KEY_LEFT):
            motor.motor_left = -1
            motor.motor_right = 1
            rospy.loginfo ("\u2190\u2190\u2190\u2190 left turn \u2190\u2190\u2190\u2190")
        elif (keyPress == KEY_RIGHT):
            motor.motor_left = 1
            motor.motor_right = -1
            rospy.loginfo ("\u2192\u2192\u2192\u2192 right turn \u2192\u2192\u2192\u2192")
        elif ((keyPress == KEY_S) or (keyPress == KEY_S2)):
            motor.motor_left = 0
            motor.motor_right = 0
            rospy.loginfo ("\u26d4 \u26d4 \u26d4 \u26d4 Stop robot \u26d4 \u26d4 \u26d4 \u26d4")
        elif ((keyPress == KEY_Q) or (keyPress == KEY_Q2)):
            print("Quiting ...")
            break
        
        pub.publish(motor)
        oldKey = keyPress
if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass