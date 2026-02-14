# conways-game-of-life

Interactive Conway’s Game of Life simulator built with Python and Pygame, featuring adjustable speed, wrapping modes, and a polished UI.

<img src="Assets/screenshot.png" alt="Conway's Game of Life screenshot" width="900">

## Features

- **Start / Pause** simulation
- **Step** one generation at a time
- **Clear** the grid
- **Randomize** the grid with a configurable density (in code)
- **Speed control** (generations per second)
- **Wrap toggle** (toroidal wrapping on/off)
- Live stats: **generation**, **alive cell count**, **grid size**, **speed**, **wrap mode**
- Mouse drawing:
  - **Left-click / drag:** paint cells alive
  - **Right-click / drag:** erase cells

## Controls

### Keyboard
- **Space** — Start / Pause
- **N** — Step one generation
- **C** — Clear
- **R** — Randomize
- **W** — Toggle wrapping

### Mouse
- **LMB** — paint (toggle/paint alive depending on build)
- **RMB** — erase

## Getting Started

### Requirements
- Python 3.9+ recommended
- Pygame

### Install
```bash
pip install pygame
