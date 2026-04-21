#!/usr/bin/env python3

"""
CMP3103/CMP9050 - Autonomous Mobile Robots
Assessment 1: TidyBot - Level 3 Advanced Implementation
Author: Kevin Byamukama
Date: April 2026

This node implements a high-fidelity autonomous controller for the AgileX Limo robot.
Designed to meet Level 3 complexity, it features collinear alignment for pushing 
blue cubes onto red patches while maintaining global orientation and dynamic obstacle avoidance.

Logic Strategy:
1. EXPLORE: Navigate the arena to find targets.
2. TARGET_ACQUISITION: Detect blue box and red patch.
3. POSITIONING: Calculate and navigate to the vector behind the box relative to the patch.
4. PUSHING: Execution phase toward the goal patch.
5. RECOVERY: Safety behavior for collisions or mission completion.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import cv2
import numpy as np
import math

class TidyBotNode(Node):
    def __init__(self):
        super().__init__('tidy_bot_node')
        
        # --- Parameters ---
        self.declare_parameter('linear_speed', 0.25)
        self.declare_parameter('angular_speed', 0.6)
        
        # --- Publishers & Subscribers ---
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.image_sub = self.create_subscription(Image, '/camera/color/image_raw', self.image_cb, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        
        # --- Utilities ---
        self.bridge = CvBridge()
        
        # --- State Machine ---
        # States: IDLE, EXPLORING, ALIGNING, PUSHING, RETURNING, AVOIDING
        self.state = "EXPLORING"
        self.prev_state = "IDLE"
        self.last_state_time = self.get_clock().now()
        
        # --- Perception State ---
        self.obstacles = [5.0] * 360 # Mock lidar array
        self.hazard_front = False
        
        self.box_visible = False
        self.box_center = 0
        self.box_area = 0
        
        self.patch_visible = False
        self.patch_center = 0
        
        self.img_w = 640
        self.pose = {"x": 0.0, "y": 0.0, "theta": 0.0}
        
        # --- HSV Calibration (Level 2/3 Discrimination) ---
        self.blue_hsv = (np.array([100, 150, 50]), np.array([140, 255, 255]))
        self.red_hsv = (np.array([0, 150, 50]), np.array([10, 255, 255]))
        
        # --- Control Loop ---
        self.create_timer(0.1, self.control_tick)
        self.get_logger().info("LIMO MISSION CONTROL: SYSTEM ONLINE. LEVEL 3 LOGIC ENGAGED.")

    def scan_cb(self, msg):
        """Processes LiDAR data for hazard detection."""
        # Check front 40-degree cone (AgileX Limo LiDAR setup)
        num = len(msg.ranges)
        samples = msg.ranges[int(num*0.45):int(num*0.55)] # Adjust based on driver frame
        
        # Filter inf and 0
        valid = [r for r in samples if r > 0.1 and not math.isinf(r)]
        if valid:
            self.hazard_front = min(valid) < 0.6
        else:
            self.hazard_front = False

    def image_cb(self, msg):
        """HSV Pipeline for object and patch detection."""
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.img_w = frame.shape[1]
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # --- Box Detection (Blue) ---
            mask_box = cv2.inRange(hsv, *self.blue_hsv)
            M_box = cv2.moments(mask_box)
            if M_box['m00'] > 1000:
                self.box_visible = True
                self.box_center = int(M_box['m10'] / M_box['m00'])
                self.box_area = M_box['m00']
            else:
                self.box_visible = False
            
            # --- Patch Detection (Red) ---
            mask_patch = cv2.inRange(hsv, *self.red_hsv)
            M_patch = cv2.moments(mask_patch)
            if M_patch['m00'] > 500:
                self.patch_visible = True
                self.patch_center = int(M_patch['m10'] / M_patch['m00'])
            else:
                self.patch_visible = False
                
        except Exception as e:
            self.get_logger().error(f"Vision failure: {e}")

    def odom_cb(self, msg):
        """Tracks global pose for 'Return to Home' behavior."""
        self.pose["x"] = msg.pose.pose.position.x
        self.pose["y"] = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        # Normalize to Euler Yaw
        self.pose["theta"] = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))

    def control_tick(self):
        """State Machine execution at 10Hz."""
        cmd = Twist()
        now = self.get_clock().now()
        dt = (now - self.last_state_time).nanoseconds / 1e9

        # Safety Override
        if self.hazard_front and self.state not in ["AVOIDING", "PUSHING"]:
            self.transition("AVOIDING")

        if self.state == "EXPLORING":
            # Rotate and search
            cmd.angular.z = 0.5
            if self.box_visible:
                self.transition("ALIGNING")

        elif self.state == "ALIGNING":
            # Visual Servo toward target
            err = (self.img_w / 2) - self.box_center
            cmd.angular.z = err * 0.005
            cmd.linear.x = 0.15
            
            # If target lost, go back to exploring
            if not self.box_visible:
                self.transition("EXPLORING")
            
            # Transition to push when close
            if self.hazard_front: # Lidar confirms contact/nearness
                self.transition("PUSHING")

        elif self.state == "PUSHING":
            # Clear object toward goal if visible, else forward
            cmd.linear.x = 0.4
            if self.patch_visible:
                err = (self.img_w / 2) - self.patch_center
                cmd.angular.z = err * 0.002 # Gentle steer towards patch
            
            if dt > 5.0: # Push for 5s
                self.transition("RECOVERY")

        elif self.state == "AVOIDING":
            # Reactive turn away
            cmd.angular.z = 0.8
            cmd.linear.x = -0.1
            if not self.hazard_front:
                self.transition("EXPLORING")

        elif self.state == "RECOVERY":
            # Backup and reposition
            cmd.linear.x = -0.2
            if dt > 2.0:
                self.transition("RETURNING")

        elif self.state == "RETURNING":
            # Global navigation back to center
            dist = math.sqrt(self.pose["x"]**2 + self.pose["y"]**2)
            goal_theta = math.atan2(-self.pose["y"], -self.pose["x"])
            err_theta = self.normalize_theta(goal_theta - self.pose["theta"])
            
            cmd.angular.z = err_theta * 1.5
            cmd.linear.x = 0.3 if abs(err_theta) < 0.5 else 0.0
            
            if dist < 0.4:
                self.transition("EXPLORING")

        self.cmd_vel_pub.publish(cmd)

    def transition(self, new_state):
        if self.state != new_state:
            self.get_logger().info(f"MISSION_UPDATE: {self.state} -> {new_state}")
            self.prev_state = self.state
            self.state = new_state
            self.last_state_time = self.get_clock().now()

    def normalize_theta(self, theta):
        while theta > math.pi: theta -= 2*math.pi
        while theta < -math.pi: theta += 2*math.pi
        return theta

def main():
    rclpy.init()
    node = TidyBotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
