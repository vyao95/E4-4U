player = 'o'
enemy = 'x'
empty = '.'
width = 7
height = 6


#Connect 4 Board Object
class Board:

    #Create new board
    def __init__(self):
        self.state = {}
        for col in range(width):
            for row in range(height):
                self.state[col,row] = empty


    def print_board(self,state):
        for i in range(height-1,-1,-1):
            for j in range(0,width):
                print(str(state[(j,i)]) + " ", end="")
            print()
        print()

    def do_move(self,state,player,move):
        if move in state:
            if move in self.get_valid_moves(state):
                if state[move] == empty:
                    state[move] = player
                else:
                    print("do_move: Tried to do " + str(move) + " but position is " + str(state[move]))
            else:
                print("do_move: Not a valid move")
        else:
            print("do_move: Move not in board.")

        return state

    #Get moves you can do for next turn
    def get_valid_moves(self,state):
        valid_moves = []
        for col in range(width):
            for row in range(height):
                if state[col,row] == empty:
                    valid_moves.append((col,row))
                    break
        return valid_moves

    #check the valid moves and see if any are moves that will make you win
    def get_winning_moves(self,state,valid_moves=[]):
        winning_moves = []
        if len(valid_moves) == 0: # this will let us use our own valid moves if we choose to optimize stuff
            valid_moves = self.get_valid_moves(state)
        for move in valid_moves:
            turn = state[move]
            if turn == '.':
                continue
            winnable = 0
            # check vertical win
            if move[1] > 2:
                for i in range(1,4):
                    if (state[(move[0],move[1]-i)] == turn):
                        if winnable == 2:
                            winning_moves.append((move,turn))
                        else:
                            winnable += 1
                    else:
                        break

            winnable = 0
            #horizontal win
            for k in range(-1,2,2): # check to both left and right
                if move not in winning_moves: # haven't already found win from one direction
                    for i in range(1,4):
                        if (move[0]-i*k,move[1]) in state: # check 3 left/right
                            if (state[(move[0]-i*k,move[1])] == turn):
                                if winnable == 2:
                                    winning_moves.append((move,turn))
                                    break
                                else:
                                    winnable += 1
                            else:
                                break

            winnable = 0
            # / win
            for k in range(-1,2,2): # check bottom left and top right directions
                if move not in winning_moves: # haven't already found win from one direction
                    for i in range(1,4):
                        if (move[0]-i*k,move[1]-i*k) in state:
                            if (state[(move[0]-i*k,move[1]-i*k)] == turn):
                                if winnable == 2:
                                    winning_moves.append((move,turn))
                                    break
                                else:
                                    winnable += 1
                            else:
                                break

            winnable = 0
            # \ win
            for k in range(-1,2,2): # check bottom left and top right directions
                if move not in winning_moves: # haven't already found win from one direction
                    for i in range(1,4):
                        if (move[0]-i*k,move[1]+i*k) in state:
                            if (state[(move[0]-i*k,move[1]+i*k)] == turn):
                                if winnable == 2:
                                    winning_moves.append((move,turn))
                                    break
                                else:
                                    winnable += 1
                            else:
                                break

        return winning_moves

    def is_ended(self,state):
        last_moves = []
        for col in range(width):
            for row in range(height):
                if state[col,row] == empty: # if we reach an empty spot (going up vertically)
                    if (col,row-1) in state: # then add the spot right before empty spot
                        last_moves.append((col,row-1))
                    break
                elif row == height - 1: # if we reach the top
                    last_moves.append((col,row))

        won = self.get_winning_moves(state,last_moves)
        if len(won) == 0:
            return (False,None)
        else:
            return (True,won[0][1])


b = Board()
for i in range(0,3):
    for j in range(0,3-i):
        b.do_move(b.state,enemy,(i,j))
b.state[0,3] = player
b.state[1,2] = player
b.state[2,1] = player
b.state[3,0] = player
b.print_board(b.state)

print(b.get_valid_moves(b.state))
print(b.get_winning_moves(b.state))
print(b.is_ended(b.state))
