from MCTS import MCTS
import connect4
from random import choice
import time

player = connect4.player
enemy = connect4.enemy

b = connect4.Board()
state = b.state
j=0

while not b.is_ended(b.state)[0]:
    if j%2 == 0:
        start = time.time()
        nextmove=MCTS(b.state)
        end = time.time()
        print("Total time: " + str(end - start))
        state = b.do_move(state,player,nextmove)
    else:
        # b.print_board(state)
        # print("0 1 2 3 4 5 6")
        # col = int(input())
        # row = int(input())
        # move = (col,row)
        # state = b.do_move(state,enemy,move)
        state = b.do_move(state,enemy,choice(b.get_valid_moves(state)))
    b.print_board(state)
    j += 1
    

print(b.is_ended(b.state))