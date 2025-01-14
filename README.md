# Autonomous Delivery Robot

A Python-based simulation of an autonomous delivery robot that navigates through a maze-like environment to deliver packages to multiple destinations while avoiding obstacles.

## Features

- Interactive 15x15 grid-based environment
- A* pathfinding algorithm for optimal route planning
- Dynamic obstacle and goal generation
- Real-time visualization using Pygame
- Multiple delivery points handling
- Save and load maze configurations
- Random vehicle (obstacle) generation
- Dynamic goal node management

## Requirements

- Python 3.x
- Pygame >= 2.5.0
- NumPy >= 1.24.0

You can install all required dependencies using:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Autonomous-Delivery-Robot.git
cd Autonomous-Delivery-Robot
```

2. Install the required dependencies:
```bash
pip install pygame numpy
```

## Usage

Run the main simulation:
```bash
python Maze.py
```

### Controls
- Left Mouse Click: Place/Remove walls
- Right Mouse Click: Set robot position
- Middle Mouse Click: Add/Remove delivery points
- Enter: Start the simulation
- ESC: Exit the program

## Project Structure

- `Maze.py`: Main simulation file containing the robot's logic and visualization
- `maze.txt`: Saved maze configuration file
- `Maze1/`: Directory containing additional maze configurations

## Features in Detail

### Pathfinding
- Implements A* algorithm for optimal path planning
- Calculates heuristic distances using Euclidean distance
- Dynamically updates path when obstacles are encountered

### Environment
- 15x15 grid-based world
- Support for multiple types of cells:
  - Empty spaces (traversable)
  - Walls (obstacles)
  - Vehicle positions (dynamic obstacles)
  - Goal nodes (delivery points)
  - Robot position

### Visualization
- Real-time rendering using Pygame
- Color-coded cells for different elements:
  - Walls
  - Path
  - Robot
  - Delivery points
  - Obstacles

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Last Updated

2025-01-14