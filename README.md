# Connect 4

This is a simple recreation of the
classic game Connect 4 made in Python.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Screenshots](#screenshots)

## Introduction

Connect 4 is a two-player connection game 
in which players take turns dropping colored 
discs into a grid. The objective is to connect 
four of one's own discs of the same color next 
to each other vertically, horizontally, or diagonally.

## Features

### 1. User interface
There are 2 types of UIs implemented: 
- Console-based user interface for easy interaction 
- Graphical user interface built with Pygame 

The user can choose which UI to use by editing the main file
```python
    # In main.py
    
    if __name__ == '__main__':
        # Assign to this variable True to use the Console UI;
        #leave it as is to use the GUI 
        console_mode = False
``` 

### 2. Game modes
The user can choose from two game modes: Versus Player and Versus Computer
### 3. AI
This project extends the classic game by adding an AI opponent, which comes in 3 difficulties.

The AI is made using the Minimax algorithm, and has the following optimisations:
- Alpha-beta pruning
- Doesn't make 1 move blunders
- Prioritises winning as early as possible, or losing as late as possible
- Using bit-strings in the internal representation of the board
## Installation

To run the Connect 4 game, you need to have Python and Pygame installed on your system. You can install Pygame using pip:

```bash
pip install pygame
```

Clone this repository to your local machine:
```bash
git clone
```
Run the main script
```bash
python main.py
```