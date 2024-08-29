import cv2
import pyrealsense2
from realsense_depth import *
import numpy as np
import math

point1 = None
 
click_count = 0


    
def show_distance(event, x, y, args, params):
    global point1, point2, click_count
    if event == cv2.EVENT_LBUTTONDOWN:
        point1 = (x, y)
        
        

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    height, width = color_frame.shape[:2]
    point2 = (width // 2, height // 2)

    # Show distance for the two points
    if point1:
        cv2.circle(color_frame, point1, 4, (0, 0, 255), -1)
        distance1 = depth_frame[point1[1], point1[0]]
        cv2.putText(color_frame, "P1: {}mm".format(distance1), (point1[0], point1[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    
    if point2:
        cv2.circle(color_frame, point2, 4, (0, 255, 0), -1)
        distance2 = depth_frame[point2[1], point2[0]]
        cv2.putText(color_frame, "P2: {}mm".format(distance2), (point2[0], point2[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    
    if point1 and point2:
        cv2.line(color_frame, point1, point2, (255, 0, 0), 2)
        # Calculate Euclidean distance
        height = 100
        diff = distance2 - np.sqrt(distance1**2 - height**2)
        angle_radians = math.atan2(height,diff)
        angle_degrees = math.degrees(angle_radians)
        
        
        dist = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        depth_diff = abs(distance1 - distance2)
        total_distance = np.sqrt(dist**2 + depth_diff**2)
        midpoint = ((point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2)
        
        print(angle_degrees)
    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    
    
    key = cv2.waitKey(1)
    if key == 27:
        break
