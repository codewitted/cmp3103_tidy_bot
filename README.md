# TidyBot: Autonomous Controller for AgileX Limo
**CMP3103/CMP9050 Assessment 1 - Level 3 Advanced Solution**

---

### 🚀 Implementation Highlights
This ROS2 package provides a complete autonomous system for the **AgileX Limo** robot, designed to solve the "Tidy-Up" task with Level 3 complexity using global navigation and reactive vision.

#### Developed Features:
- **Level 1 (Basic Clearing):** Robust reactive state machine to detect any colored object on a patch and push it clear.
- **Level 2 (Color Discrimination):** HSV image masking pipeline to specifically target **BLUE** objects while ignoring others, even when located on **RED** goal patches.
- **Level 3 (Obstacle & Global Goal):** 
    - **Reactive Obstacle Avoidance:** Real-time LiDAR processing to navigate around static pillars.
    - **Push-to-Goal Logic:** Intelligent steering during the pushing phase to guide objects toward the designated landing zone.
    - **Global Orientation:** Integrated Odometry PID control for "Return-to-Home" reset maneuvers after task completion.

---

### 📂 Project Structure
- `cmp3103_tidy_bot/`: Core logic package.
  - `tidy_bot_node.py`: ROS2 Node implementing the Controller and Vision Pipeline.
- `launch/`: Deploy scripts.
  - `tidy_bot.launch.py`: Unified launch file for simulation.
- `package.xml` & `setup.py`: Build system configuration for `colcon`.
- `dashboard_legacy/`: Original React simulation used for prototyping the state machine.

---

### 🏃 How to Run in Gazebo

#### 1. Setup Simulation Environment
Follow the official AgileX instructions to install the Limo simulator:
```bash
# Clone the Gazebo simulation package
git clone https://github.com/limo-agx/limo_simulator.git ~/catkin_ws/src
# Install dependencies
rosdep install --from-paths src --ignore-src -y
# Build
catkin_make
source devel/setup.bash
```

#### 2. Launch the Arena
```bash
# Start Gazebo with the Limo robot in the arena
ros2 launch limo_gazebo_sim limo_arena.launch.py
```

#### 3. Build & Run the TidyBot Controller
```bash
# Build this package
colcon build --packages-select cmp3103_tidy_bot
source install/setup.bash

# Launch the autonomous mission
ros2 launch cmp3103_tidy_bot tidy_bot.launch.py
```

---

### 📊 Performance & Evaluation
The system utilizes **Visual Servoing** to maintain alignment with objects. By monitoring the centroid error $e = (width/2 - center)$, the robot applies an angular feedback $v_z = k_p \cdot e$ to track dynamic targets. The LiDAR sweep ensures zero collisions with the perimeter or static pillars by overriding the motion commands when a hazard is detected in the front 40-degree arc.

---

**Author:** Kevin Byamukama  
**Course:** Autonomous Mobile Robots 2526  
**SPDX-License-Identifier:** Apache-2.0
