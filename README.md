# E4-4U

E4-4U is a bot that autonomously plays Connect 4 games online for you.

Its decisions are based on a Monte Carlo Tree Search algorithm which essentially simulates possible game outcomes based on your possible moves and uses those outcomes to determine your next best move.

How this all works:

1. The user runs the program and is prompted to click on the upper left and bottom right corners of the game board when it is their first turn.
2. E4-4U takes a screenshot of the board (using pyscreenshot) based on those coordinates.
3. Then, it processes the screenshot into an initial game state.
4. Our bot determines your next best move based on the MCTS algorithm and then performs it automatically (using pyautogui to take control of the mouse).
4. Steps 2-4 are repeated until the game is over and you've won!

Demo:

https://www.youtube.com/watch?v=J1TGxDdrq2c
