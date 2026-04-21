# TidyBot: Autonomous Controller for AgileX Limo
**CMP3103/CMP9050 Assessment 1 - Level 3 Advanced Solution**

---

### 🚀 Implementation Highlights
This ROS 2 package provides a complete autonomous system for the **AgileX Limo** robot, designed to solve the "Tidy-Up" task with Level 3 complexity using global navigation and reactive vision.

#### Developed Features:
- **Level 1 (Basic Clearing):** Robust reactive state machine to detect any colored object on a patch and push it clear.
- **Level 2 (Color Discrimination):** Enhanced HSV image masking pipeline to specifically target **BLUE** objects while ignoring others, even when located on **RED** goal patches.
- **Level 3 (Obstacle & Global Goal):** 
    - **Reactive Obstacle Avoidance:** Multi-sector LiDAR processing to navigate around static pillars and walls.
    - **Push-to-Goal Logic:** Balanced visual servoing during the pushing phase to guide objects toward the red landing zones.
    - **Global Localization:** Odometry-based origin return logic to reposition for the next search iteration.

---

### 📂 Project Structure
- `cmp3103_tidy_bot/`: Core ROS 2 Python package.
  - `tidy_bot_node.py`: Main controller implementing the state machine and vision pipeline.
- `launch/`: Deploy scripts.
  - `tidy_bot.launch.py`: ROS 2 launch file for simulation.
- `setup.py` & `package.xml`: Standard ROS 2 build configuration.

---

### 🏃 Build and Run

#### 1. Environment Requirements
**DO NOT RUN IN WINDOWS POWERSHELL.** Use a proper Linux environment:
- Provided DevContainer
- Ubuntu 22.04 + ROS 2 Humble
- WSL2 (Ubuntu)

#### 2. Workspace Setup
Open a Linux terminal and create your workspace:
```bash
mkdir -p ~/tidybot_ws/src
cd ~/tidybot_ws/src

# Clone the simulation environment
git clone https://github.com/limo-agx/limo_simulator.git

# Clone this repository (assuming your current folder is src)
# git clone <your_repo_url>
```

#### 3. Build with Colcon
```bash
cd ~/tidybot_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

#### 4. Launch Simulation
In a new terminal:
```bash
source /opt/ros/humble/setup.bash
source ~/tidybot_ws/install/setup.bash
ros2 launch limo_gazebo_sim limo_arena.launch.py
```

#### 5. Launch TidyBot Controller
In another new terminal:
```bash
source /opt/ros/humble/setup.bash
source ~/tidybot_ws/install/setup.bash
ros2 launch cmp3103_tidy_bot tidy_bot.launch.py
```

---

### 📊 System Logic
The controller uses a **Hybrid State Machine**:
- **Vision:** Utilizes morphology-cleaned HSV masks to track centroids. Red detection is hardened by joining masks for both 0-10 and 170-180 hue ranges.
- **Safety:** LiDAR hazard detection is intelligently suppressed during `ALIGNING` and `PUSHING` states to allow contact with target objects while remaining active for pillar avoidance.

**Author:** Kevin Byamukama  
**Course:** Autonomous Mobile Robots 2526  
**SPDX-License-Identifier:** Apache-2.0
