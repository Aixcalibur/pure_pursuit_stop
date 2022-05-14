#!/usr/bin/env python
# license removed for brevity
from pkg_resources import yield_lines
import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped

stopSigns = [(46,-11.5), (35,-53.6), (2,-27.7)]
stopSignIndex = 0
stopStart = 0
pub = rospy.Publisher('purepursuit/stop', Bool, queue_size=10)

def callback(data):

    global stopSignIndex
    global stopStart
    global pub

    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose)

    if ((abs(data.pose.position.x-stopSigns[stopSignIndex][0]) < 1) and (abs(data.pose.position.y-stopSigns[stopSignIndex][1]) < 1)):
        stopEnd = rospy.get_time()

        if stopEnd - stopStart >= 3:

            if stopSignIndex >= len(stopSigns)-1:
                stopSignIndex = 0
            else: 
                stopSignIndex += 1

            pub.publish(False)
        else:
            pub.publish(True)
    else:
        stopStart = rospy.get_time()

def listener():

    
    
    rospy.init_node('stopbehavior', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    rospy.Subscriber("/current_pose", PoseStamped, callback)
    # spin() simply keeps python from exiting until this node is stopped


    

    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass