#!/usr/bin/env python3

"""
CMP3103/CMP9050 - Autonomous Mobile Robots
Assessment 1: TidyBot - Level 3 Advanced Implementation
Author: Kevin Byamukama
Date: April 2026

This node implements a high-fidelity autonomous controller for the AgileX Limo robot.
Optimized for the official Gazebo simulation.
"""

import math
import cv2
import numpy as np
import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge


class TidyBotNode(Node):
    def __init__(self):
        super().__init__('tidy_bot_node')

        self.declare_parameter('linear_speed', 0.25)
        self.declare_parameter('angular_speed', 0.6)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Image, '/camera/color/image_raw', self.image_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

        self.bridge = CvBridge()

        self.state = "EXPLORING"
        self.prev_state = "IDLE"
        self.last_state_time = self.get_clock().now()

        self.hazard_front = False
        self.box_visible = False
        self.box_center = 0
        self.box_area = 0
        self.patch_visible = False
        self.patch_center = 0
        self.img_w = 640

        self.pose = {"x": 0.0, "y": 0.0, "theta": 0.0}

        # HSV Thresholds
        self.blue_lower = np.array([100, 120, 50])
        self.blue_upper = np.array([140, 255, 255])

        # Red wraps around HSV 0/180
        self.red1_lower = np.array([0, 120, 70])
        self.red1_upper = np.array([10, 255, 255])
        self.red2_lower = np.array([170, 120, 70])
        self.red2_upper = np.array([180, 255, 255])

        self.create_timer(0.1, self.control_tick)
        self.get_logger().info("TidyBot node started. Ready for mission.")

    def scan_cb(self, msg):
        """Processes LiDAR for hazard detection in the front cone."""
        raw = np.array(msg.ranges, dtype=np.float32)
        n = len(raw)
        
        # FRONT CONE: First and last 10 degrees sector
        # (Limo LiDAR usually starts at 0 straight ahead or 180 depending on driver)
        # Assuming standard ROS LaserScan where 0 is ahead
        sector = max(1, n // 18) # ~20 deg total
        front_indices = list(range(0, sector)) + list(range(n - sector, n))
        
        front_vals = [raw[i] for i in front_indices if np.isfinite(raw[i]) and raw[i] > 0.10]

        self.hazard_front = len(front_vals) > 0 and min(front_vals) < 0.45

    def image_cb(self, msg):
        """HSV Vision Pipeline with noise cleanup."""
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            self.img_w = frame.shape[1]

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            kernel = np.ones((5, 5), np.uint8)

            # --- Target detection (Blue Box) ---
            mask_box = cv2.inRange(hsv, self.blue_lower, self.blue_upper)
            # Morphology to clean noise
            mask_box = cv2.morphologyEx(mask_box, cv2.MORPH_OPEN, kernel)
            mask_box = cv2.morphologyEx(mask_box, cv2.MORPH_CLOSE, kernel)
            M_box = cv2.moments(mask_box)

            if M_box["m00"] > 1200:
                self.box_visible = True
                self.box_center = int(M_box["m10"] / M_box["m00"])
                self.box_area = M_box["m00"]
            else:
                self.box_visible = False
                self.box_area = 0

            # --- Goal detection (Red Patch) ---
            mask_patch1 = cv2.inRange(hsv, self.red1_lower, self.red1_upper)
            mask_patch2 = cv2.inRange(hsv, self.red2_lower, self.red2_upper)
            mask_patch = mask_patch1 | mask_patch2 # Combine both red ranges
            mask_patch = cv2.morphologyEx(mask_patch, cv2.MORPH_OPEN, kernel)
            mask_patch = cv2.morphologyEx(mask_patch, cv2.MORPH_CLOSE, kernel)
            M_patch = cv2.moments(mask_patch)

            if M_patch["m00"] > 2000:
                self.patch_visible = True
                self.patch_center = int(M_patch["m10"] / M_patch["m00"])
            else:
                self.patch_visible = False

        except Exception as e:
            self.get_logger().error(f"Vision failure: {e}")

    def odom_cb(self, msg):
        """Pose tracking for origin reset."""
        self.pose["x"] = msg.pose.pose.position.x
        self.pose["y"] = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        # Yaw conversion
        self.pose["theta"] = math.atan2(
            2 * (q.w * q.z + q.x * q.y),
            1 - 2 * (q.y * q.y + q.z * q.z)
        )

    def control_tick(self):
        """High-level behavior state machine."""
        cmd = Twist()
        now = self.get_clock().now()
        dt = (now - self.last_state_time).nanoseconds / 1e9

        # --- GLOBAL BEHAVIOR: Obstacle Avoidance (Blocked during target approach/push) ---
        if self.hazard_front and self.state not in ["AVOIDING", "ALIGNING", "PUSHING"]:
            self.transition("AVOIDING")

        if self.state == "EXPLORING":
            # Search rotation
            cmd.angular.z = self.angular_speed
            if self.box_visible:
                self.transition("ALIGNING")

        elif self.state == "ALIGNING":
            # Visual Servo to target
            if not self.box_visible:
                self.transition("EXPLORING")
            else:
                err = (self.img_w / 2) - self.box_center
                cmd.angular.z = float(err) * 0.005 # PD controller kP
                cmd.linear.x = self.linear_speed * 0.5

                # Switch to push on contact or proximity
                if self.box_area > 18000 or self.hazard_front:
                    self.transition("PUSHING")

        elif self.state == "PUSHING":
            # Execution: Push toward patch if visible
            cmd.linear.x = self.linear_speed
            if self.patch_visible:
                err = (self.img_w / 2) - self.patch_center
                cmd.angular.z = float(err) * 0.002

            if dt > 4.5: # Push complete
                self.transition("RECOVERY")

        elif self.state == "AVOIDING":
            # Reactive reverse and turn
            cmd.linear.x = -0.05
            cmd.angular.z = self.angular_speed * 1.2
            if not self.hazard_front and dt > 1.0:
                self.transition("EXPLORING")

        elif self.state == "RECOVERY":
            # Back up after push
            cmd.linear.x = -0.15
            if dt > 1.5:
                self.transition("RETURNING")

        elif self.state == "RETURNING":
            # Navigate back to origin (0,0)
            dist = math.sqrt(self.pose["x"] ** 2 + self.pose["y"] ** 2)
            goal_theta = math.atan2(-self.pose["y"], -self.pose["x"])
            err_theta = self.normalize_theta(goal_theta - self.pose["theta"])

            cmd.angular.z = 1.2 * err_theta
            cmd.linear.x = 0.15 if abs(err_theta) < 0.4 else 0.0

            if dist < 0.4:
                self.transition("EXPLORING")

        self.cmd_vel_pub.publish(cmd)

    def transition(self, new_state):
        if self.state != new_state:
            self.get_logger().info(f"STATE_TRANSITION: {self.state} -> {new_state}")
            self.prev_state = self.state
            self.state = new_state
            self.last_state_time = self.get_clock().now()

    @staticmethod
    def normalize_theta(theta):
        while theta > math.pi: theta -= 2 * math.pi
        while theta < -math.pi: theta += 2 * math.pi
        return theta


def main(args=None):
    rclpy.init(args=args)
    node = TidyBotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
