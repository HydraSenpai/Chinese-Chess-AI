import unittest
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

    def test_in_check(self):
        agent = Agent()
        
        # ROOK CHECKS
        # Board with K in check from r from front        
        temp_board = '0000k0000/0000r0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check from r from left
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/r000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check from r from right
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K000r'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K not in check as p blocks r 
        temp_board = '0000k0000/0000r0000/0000p0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.in_check(board, True))
        
        # CANNON CHECKS
        # Board with K not in check by c at [1][4]
        temp_board = '0000k0000/0000c0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertFalse(agent.in_check(board, True))
        # Board with K in check by c at [1][4]
        temp_board = '0000k0000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check by c at left
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/cp00K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check by c at right
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K00pc'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check by c at right over own piece
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000K00Pc'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        
        
        # HORSE CHECKS
        # Board with K in check by h at [7][3]
        temp_board = '0000k0000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000h00000/000000000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check by h at [8][7]
        temp_board = '0000k0000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/000000h00/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        
        # PAWN CHECKS
        # Board with K in check by p at [8][4] at front
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000p0000/0000K0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check by p at [9][3] at left
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000pK0000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        # Board with K in check by p at [9][5] at right
        temp_board = '0000k0000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/000000000/0000Kp000'
        board = temp_board.split('/')
        self.assertTrue(agent.in_check(board, True))
        
        
        
if __name__ == '__main__':
    unittest.main()