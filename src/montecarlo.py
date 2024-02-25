from node import Node
from methods import *

class SearchTree:
    def __init__(self, node):
        self.root = node

    def best_action(self, simulations_number):
        print('best action')
        for _ in range(0, simulations_number):
            # Find next node (state) to rollout
            v = self.tree_policy()
            # print('found node to expand')
            reward = v.rollout()
            # print('rolled out node')
            v.backpropagate(reward)
            # print('backpropogated')
        return self.root.best_child(c_param=1.4).state
    
    
    # This method is used to find the next node to rollout by going down tree to find node with UCT (Upper Confidence Bound)
    def tree_policy(self):
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