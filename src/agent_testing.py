import unittest
import math
import time
from agent import Agent

class TestAgent(unittest.TestCase):
    
    # Test that terminal state is correctly identified
    def test_terminal_state(self):
        agent = Agent()
        # Board with K in checkmate by 2 rooks
        temp_board = 'R0eakaehr/000000000/000000000/p0p0p0p0p/000000000/000000000/000000000/000000000/00000000r/0000K000r'
        board = temp_board.split('/')
        self.assertTrue(agent.is_terminal_state(board, True))
        self.assertFalse(agent.is_terminal_state(board, False))
        
        # Board with K in check by 1 rook but not checkmate as K can move forward one square to escape check
        temp_board = 'R0eakaehr/000000000/000000000/p0p0p0p0p/000000000/000000000/000000000/000000000/000000000/0000K000r'
        board = temp_board.split('/')
        self.assertFalse(agent.is_terminal_state(board, True))
        
        # Board with K in check by 2 cannons but also king and rook to block side escapes
        temp_board = '00ek0r000/000000000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_terminal_state(board, True))
        
        # Board with K in check by 2 cannons and also king but no rook so has one escape to the side
        temp_board = '00ek00000/000000000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.is_terminal_state(board, True))
        
        # Board with K in between 2 rooks so can't move (stalemate)
        temp_board = '000k00000/000000000/000000000/000000000/000000000/000000000/000000000/000r00000/0000K0000/00000r000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_terminal_state(board, True))
        
        # Board with just kings alive
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.is_terminal_state(board, True))
        
    def test_evaluation(self):
        agent = Agent()
        
        # Board with equal pieces
        temp_board = '0000k0000/0000r0000/000000000/000000000/000000000/000000000/000000000/000000000/0000R0000/0000K0000'
        board = temp_board.split('/')
        self.assertEqual(agent.evaluation(board, True), agent.evaluation(board, False))
        
        # Board with K side having an extra R so should have a higher evaluation
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000R0000/0000K0000'
        board = temp_board.split('/')
        self.assertGreater(agent.evaluation(board, True), agent.evaluation(board, False))
        
        # Board with K side having an the R closer to the king so should have a higher evaluation
        temp_board = '0000k0000/0000r0000/0000R0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertGreater(agent.evaluation(board, True), agent.evaluation(board, False))
        
        # Board with K side having the knight in a better position so should have a higher evaluation
        temp_board = '0h00k0000/0000r0000/000000000/000000000/000000000/000000000/000000000/00H000000/0000R0000/0000K0000'
        board = temp_board.split('/')
        self.assertGreater(agent.evaluation(board, True), agent.evaluation(board, False))
        
        # Board with equal pieces but one is in check so should have a higher evaluation
        temp_board = '0000k0000/000r00000/000000000/000000000/000000000/000000000/000000000/000000000/0000R0000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, False))
        self.assertFalse(agent.is_check(board, True))
        self.assertGreater(agent.evaluation(board, True), agent.evaluation(board, False))
        
    def test_flying_general(self):
        agent = Agent()
        
        # Board with kings facing each other with no pieces blocking them
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.flying_general(board))
        
        # Board with kings facing each other with a piece blocking them
        temp_board = '0000k0000/000000000/000000000/000000000/0000r0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.flying_general(board))
        
        # Board with kings one block sideways apart
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/00000K000'
        board = temp_board.split('/')
        self.assertFalse(agent.flying_general(board))
        
        # Board with missing k should show a TypeError as flying general method has to find king
        temp_board = '000000000/000000000/000000000/000000000/0000r0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        with self.assertRaises(TypeError):
            agent.flying_general(board)

    def test_is_check(self):
        agent = Agent()
        
        # ROOK CHECKS
        # Board with K in check from r from front        
        temp_board = '0000k0000/0000r0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check from r from left
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/r000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check from r from right
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K000r'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K not in check as p blocks r 
        temp_board = '0000k0000/0000r0000/0000p0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.is_check(board, True))
        
        # CANNON CHECKS
        # Board with K not in check by c at [1][4]
        temp_board = '0000k0000/0000c0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.is_check(board, True))
        # Board with K in check by c at [1][4]
        temp_board = '0000k0000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check by c at left
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/cp00K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check by c at right
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K00pc'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check by c at right over own piece
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K00Pc'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        
        
        # HORSE CHECKS
        # Board with K in check by h at [7][3]
        temp_board = '0000k0000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000h00000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check by h at [8][7]
        temp_board = '0000k0000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/000000h00/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        
        # PAWN CHECKS
        # Board with K in check by p at [8][4] at front
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000p0000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check by p at [9][3] at left
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000pK0000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        # Board with K in check by p at [9][5] at right
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000Kp000'
        board = temp_board.split('/')
        self.assertTrue(agent.is_check(board, True))
        
    def test_calculate_moves(self):
        agent = Agent()
        
        # PAWN CHECKS
        # Board with P in home side so can only move forward        
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000P0000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'P', 8, 4, True, True)) == 1)    
        
        # Board with P in rival side so can move forward and sideways    
        temp_board = '0000k0000/000000000/0000P0000/000000000/000000000/000000000/000000000/000000000/0000P0000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'P', 2, 4, True, True)) == 3)    
        
        # Board with P in rival side so can only move forward due to flying general rule    
        temp_board = '0000k0000/000000000/0000P0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'P', 2, 4, True, True)) == 1) 
        
        # Board with P in rival side so can move forward and sideways due to False being passed in so check and flying general checks aren't checked    
        temp_board = '0000k0000/000000000/0000P0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'P', 2, 4, True, False)) == 3)
        
        # KNIGHT CHECKS
        # Board with H free to move    
        temp_board = '0000k0000/0000P0000/000000000/000000000/0000H0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'H', 4, 4, True, True)) == 8)
        self.assertTrue(len(agent.calculate_moves(board, 'H', 4, 4, True, False)) == 8)
        
        # Board with H on wall so cant move off board   
        temp_board = '0000k0000/0000P0000/000000000/000000000/00000000H/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'H', 4, 8, True, True)) == 4)
        
        # Board with H one from wall so cant move off board   
        temp_board = '0000k0000/0000P0000/000000000/000000000/0000000H0/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'H', 4, 7, True, True)) == 6)
        
        # Board with H blocked on all sides so cant move   
        temp_board = '0000k0000/0000P0000/000000000/0000p0000/000pHp000/0000p0000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'H', 4, 4, True, True)) == 0)
        
        # Board with H blocked on 3 sides so has 2 possible moves downwards   
        temp_board = '0000k0000/0000P0000/000000000/0000p0000/000pHp000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'H', 4, 4, True, True)) == 2)

        # ELEPHANT MOVES
        # Board with E on starting position should have 2 moves   
        temp_board = '0000k0000/0000P0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/00E0K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'E', 9, 2, True, True)) == 2)
        
        # Board with E on starting position but blocked on left should have 1 move   
        temp_board = '0000k0000/0000P0000/000000000/000000000/000000000/000000000/000000000/000000000/0E0000000/00E0K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'E', 9, 2, True, True)) == 1)
        
        # Board with E on edge of team side should have 2 moves downwards as it can't cross the river 
        temp_board = '0000k0000/0000P0000/000000000/000000000/000000000/00E000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'E', 5, 2, True, True)) == 2)
        
        # KING MOVES
        # Board with K blocked by own P and flying general so cant move
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/00000P000/00000K000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'K', 9, 5, True, True)) == 0)
        
        # Board with K which can move all directions
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/0000P0000/000000000/0000K0000/000000000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'K', 8, 4, True, True)) == 4)
        
        # Board with K which is in flying general rule so can move sideways only
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000/000000000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'K', 8, 4, True, True)) == 2)
        
        # GUARD MOVES
        # Board with K which is in flying general rule so can move sideways only
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'K', 8, 4, True, True)) == 0)
        
        # CANNON MOVES
        # Board with C in middle of board so should be able to move up and down because of flying general
        temp_board = '0000k0000/000000000/000000000/000000000/0000C0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'C', 4, 4, True, True)) == 7)
        
        # Board with C in middle of board so should be able to all directions
        temp_board = '0000k0000/000000000/000000000/000000000/0000C0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'C', 4, 4, True, False)) == 15)
        
        # Board with C blocked by 2 pieces each direction so can jump over and take a piece in each direction
        temp_board = '0000k0000/000000000/00000p000/0000p0000/00ppCpp00/0000p0000/0000p0000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'C', 4, 4, True, False)) == 4)
        
        # ROOK CHECKS
        # Board with R in middle of board so should be able to move up and down because of flying general
        temp_board = '0000k0000/000000000/000000000/000000000/0000R0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'R', 4, 4, True, True)) == 7)
        
        # Board with R in middle of board so should be able to all directions
        temp_board = '0000k0000/000000000/000000000/000000000/0000R0000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'R', 4, 4, True, False)) == 16)
        
        # Board with R blocked by a piece in each direction so can jump over and take a piece in each direction
        temp_board = '0000k0000/000000000/000000000/0000p0000/000pRp000/0000p0000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(len(agent.calculate_moves(board, 'R', 4, 4, True, False)) == 4)      
        
    def test_minimax_testing(self):
        agent = Agent()
        # Minimax should always return two items, move and value        
        temp_board = 'rhegkgehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEGKGEHR'
        board = temp_board.split('/')
        result = agent.minimax(board, 1, -math.inf, math.inf, True, {})
        self.assertTrue(len(result) == 2) 
        
        # First value should be an int as its the state score
        self.assertTrue(isinstance(result[0], int))
        
        # Second value should be an array as its the state score
        self.assertTrue(isinstance(result[1], list))
        
        # Stress test as minimax can handle large depths
        result = agent.minimax(board, 5, -math.inf, math.inf, True, {})
        self.assertTrue(len(result) == 2) 
        
        # Different depths will pick the optimal move
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/00000000R/0000K0000'
        board = temp_board.split('/')
        result1 = agent.minimax(board, 2, -math.inf, math.inf, True, {})
        result2 = agent.minimax(board, 4, -math.inf, math.inf, True, {})
        self.assertTrue(result1[1] == result2[1]) 
        
        # Depth of 3 will return optimal move in under 10 seconds
        temp_board = 'rhegkgehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEGKGEHR'
        board = temp_board.split('/')
        start_time = time.time()
        result1 = agent.minimax(board, 3, -math.inf, math.inf, True, {})
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(execution_time)
        self.assertTrue(execution_time < 10000) 
          
    def mcts_testing(self):
        pass
    
if __name__ == '__main__':
    unittest.main()