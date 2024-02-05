import numpy as np
from collections import defaultdict
from methods import *

class Node:
        def __init__(self, state, turn, parent=None):
            self._number_of_visits = 0.
            self._results = defaultdict(int)
            self.state = state
            self.parent = parent
            self.children = []
            self.turn = not turn
            self._untried_actions = []
            self._untried_actions = self.untried_actions()

        # Returns the list of untried actions from a given node
        def untried_actions(self):
            self._untried_actions = next_states(self.state, self.turn)
            return self._untried_actions

        # Returns the difference in wins - loses of a node
        @property
        def q(self):
            wins = self._results[1]
            loses = self._results[-1]
            return wins - loses

        @property
        def n(self):
            return self._number_of_visits

        # Expands the chosen node to the next state
        def expand(self):
            next_state = self._untried_actions.pop()
            child_node = Node(next_state, self.turn, parent=self)
            self.children.append(child_node)
            return child_node

        def is_terminal_node(self):
            return is_terminal_state(self.state, self.turn)

        def rollout(self):
            current_rollout_state = self.state
            current_rollout_turn = self.turn
            while not is_terminal_state(current_rollout_state, current_rollout_turn):
                possible_moves = next_states(current_rollout_state, current_rollout_turn)
                current_rollout_state = self.rollout_policy(possible_moves)
                current_rollout_turn = not current_rollout_turn
                # print_row(current_rollout_state)
            print_row(current_rollout_state)
            print('turn = ' + str(current_rollout_turn))
            return self.game_result(current_rollout_state, current_rollout_turn)

        def backpropagate(self, result):
            self._number_of_visits += 1.
            self._results[result] += 1.
            if self.parent:
                self.parent.backpropagate(result)

        def is_fully_expanded(self):
            return len(self._untried_actions) == 0

        def best_child(self, c_param=1.4):
            choices_weights = [
                (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
                for c in self.children
            ]
            return self.children[np.argmax(choices_weights)]

        def rollout_policy(self, possible_moves):
            return possible_moves[np.random.randint(len(possible_moves))]
        
        def game_result(self, state, turn):
            if self.turn == turn:
                return 1
            return -1