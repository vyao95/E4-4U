from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
import connect4

player = connect4.player
enemy = connect4.enemy
num_nodes = 1000
explore_faction = 2

def get_child_by_winrate(node):
    children = [(c,(c.wins / c.visits))
               for c in node.child_nodes.values()]
    children = sorted(children, key=lambda x: x[1])
    return children[-1][0]

def traverse_nodes(node): #, board, state, identity):
    """ Traverses the tree until we reach a leaf node.
        A leaf node is defined as any node with untried actions, NOT as in a node with no children.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'x' or 'o'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    if node.untried_actions:
        return node
    else:
        while len(node.untried_actions) == 0 and len(node.child_nodes) > 0:
            if node.turn == player:
                children = [(c,((c.wins / c.visits) +
                                 sqrt(explore_faction * log(c.parent.visits)/c.visits)))
                                 for c in node.child_nodes.values()]
            else:
                 children = [(c,((1 - (c.wins / c.visits)) +
                                  sqrt(explore_faction * log(c.parent.visits)/c.visits)))
                                  for c in node.child_nodes.values()]

            children = sorted(children, key=lambda x: x[1])
            node = children[-1][0]

            # identity = player if player_turn % 2 == 0 else enemy
            # state = board.do_move(state,identity,node.parent_action)
            # node.state = state
    return node


def expand_leaf(node, board):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    move = board.get_best_move(node.state,node.untried_actions)
    node.untried_actions.remove(move)
    new_state = board.do_move(node.state,node.turn,move)
    new_node = MCTSNode(state = new_state,
                        turn = player if node.turn == enemy else enemy,
                        parent = node,
                        parent_action = move,
                        untried_actions = board.get_valid_moves(new_state))
    node.child_nodes[move] = new_node
    return new_node


def rollout(board, node):
    """ Given the state of the game, the rollout plays out the remainder.

    Args:
        board:  The game setup.
        node:   The node for which a game will be rolled out

    Returns:    Winner of the game
    """
    state = node.state
    turn = node.turn
    game_over = (False,0)

    while not game_over[0]:
        # print("rollout:")
        # board.print_board(state)
        # print(game_over)
        move = choice(board.get_valid_moves(state))
        state = board.do_move(state, turn, move)
        turn = player if turn == enemy else enemy
        game_over = board.is_ended(state)
    return game_over[1]


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node is not None:
        if won:
            node.wins += 1
        node.visits += 1
        node = node.parent


def MCTS(board):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.

    Returns:    The action to be taken.

    """
    winning_moves = board.get_winning_moves(board.state)
    if winning_moves:
        print("E4-4U goes: " + str(winning_moves[0][0]))
        return winning_moves[0][0]
        
    root_node = MCTSNode(   state = board.state,
                            turn = player,
                            parent=None,
                            parent_action=None,
                            untried_actions=board.get_valid_moves(board.state))

    for _ in range(num_nodes):
        node = root_node

        leaf_node = traverse_nodes(node)
        if leaf_node.untried_actions:
            leaf_node = expand_leaf(leaf_node, board)
        winner = rollout(board, leaf_node)
        won = True if winner == player else False
        backpropagate(leaf_node,won)
        # board.print_board(leaf_node.state)


    action = get_child_by_winrate(root_node).parent_action
    # print(root_node.child_nodes)
    print("E4-4U goes: " + str(action))

    return action
