# 🏀 Ballie - The Bouncing Ball

A simple 2D physics-based bouncing ball simulation built with Pygame. This project demonstrates core game development concepts including a game loop, physics (gravity, friction), keyboard controls, and "squash and stretch" animation principles for a more lively, cartoon-like feel..

---

## 🌟 Features

* **Realistic Physics:** Implements gravity, acceleration, and both air and ground friction.
* **Squash and Stretch:** The ball squashes on impact and anticipates a jump, adding a dynamic and appealing animation.
* **Responsive Controls:** Move left, right, and jump.
* **Dynamic Shadow:** A simple, soft shadow that scales with the ball's shape.
* **Collision Detection:** The ball correctly bounces off the floor, ceiling, and walls.

---

## 🚀 How to Runsssss

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rohan-bhxtia/Ballie-TheBouncyGame.git
   cd Ballie-TheBouncyGame
    ```

2.  **Install the dependencies:**
    This project requires Pygame. You can install it using pip:
    ```bash
    pip install pygame
    ```

3.  **Ensure assets are present:**
    Make sure the `ball.png` file is in the same directory as `game.py`.

4.  **Run the game:**
    ```bash
    python game.py
    ```
    (Note: The game window is set to `2000x1000`. You can adjust the `WIDTH` and `HEIGHT` variables in `game.py` if needed.)

---

## 🎮 Controls

* **Left Arrow:** Move left
* **Right Arrow:** Move right
* **Up Arrow:** Jump (Hold for a moment on the ground to see the 'anticipation' squash!)

---

## 💻 Technologies Used

* **Python**
* **Pygame**
