from node import Node
from methods import *

# CODE REFERENCED FROM CHESS.COM and project code from https://ai-boson.github.io/mcts/
class SearchTree:
    def __init__(self, node):
        self.root = node

    # This method finds the best action after running simulations on nodes
    def best_action(self, simulations_number):
        print('best action')
        for _ in range(0, simulations_number):
            # Find the next state to rollout
            v = self.find_next_node()
            # print('found node to expand')
            reward = v.rollout_node()
            # print('rolled out node')
            v.backpropagate(reward)
            # print('backpropogated')
        return self.root.best_child(c_param=1.5).state
    
    
    # This method is used to find the next node to rollout by going down tree to find node with UCT (Upper Confidence Bound)
    def find_next_node(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            # Check if any children are left of current state
            if not current_node.is_fully_expanded():
                # If children available expand to the next state (go down the tree one step)
                return current_node.expand()
            else:
                # If all children have been searched pick the best child and rollout from that state again
                current_node = current_node.best_child()
        # print_row(current_node)
        return current_node