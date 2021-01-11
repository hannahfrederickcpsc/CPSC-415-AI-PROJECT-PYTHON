# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import copy
from chess_player import ChessPlayer

class hfrederi_ChessPlayer(ChessPlayer):
    our_color = 'white'
    their_color = 'black'
    piece_values = dict()
    move_values = dict()
    search_depth = 0
    old_loc = ''
    new_loc = ''
    alpha = float("-inf")
    beta = float("inf")
    search_score = 0.0
    num_turns = 0
    last_in_check = 0
    last_move = ''
    board_size = ''
    
    def __init__(self, board, color):
        super().__init__(board, color)
        if self.color == 'white':
            self.our_color = 'white'
            self.their_color = 'black'
            for place, piece in self.board.items():
                x = piece.get_notation()
                if x == 'P':
                    self.piece_values[x] = -0.1
                    self.piece_values[x.lower()] = 0.1
                elif x == 'N':
                    self.piece_values[x] = -0.2
                    self.piece_values[x.lower()] = 0.2
                elif x == 'F':
                    self.piece_values[x] = -0.3
                    self.piece_values[x.lower()] = 0.3
                elif x == 'B':
                    self.piece_values[x] = -0.4
                    self.piece_values[x.lower()] = 0.4
                elif x == 'R':
                    self.piece_values[x] = -0.5
                    self.piece_values[x.lower()] = 0.5
                elif x == 'S':
                    self.piece_values[x] = -0.6
                    self.piece_values[x.lower()] = 0.6
                elif x == 'Q':
                    self.piece_values[x] = -0.7
                    self.piece_values[x.lower()] = 0.7
                elif x == 'K':
                    self.piece_values[x] = -1.0
                    self.piece_values[x.lower()] = 1.0
                else:
                    continue
        else:
            self.our_color = 'black'
            self.their_color = 'white'
            for place, piece in self.board.items():
                x = piece.get_notation()
                if x == 'p':
                    self.piece_values[x] = -0.1
                    self.piece_values[x.upper()] = 0.1
                elif x == 'n':
                    self.piece_values[x] = -0.2
                    self.piece_values[x.upper()] = 0.2
                elif x == 'f':
                    self.piece_values[x] = -0.3
                    self.piece_values[x.upper()] = 0.3
                elif x == 'b':
                    self.piece_values[x] = -0.4
                    self.piece_values[x.upper()] = 0.4
                elif x == 'r':
                    self.piece_values[x] = -0.5
                    self.piece_values[x.upper()] = 0.5
                elif x == 's':
                    self.piece_values[x] = -0.6
                    self.piece_values[x.upper()] = 0.6
                elif x == 'q':
                    self.piece_values[x] = -0.8
                    self.piece_values[x.upper()] = 0.8
                elif x == 'k':
                    self.piece_values[x] = -1.0
                    self.piece_values[x.upper()] = 1.0
                else:
                    continue
        if len(self.board.values()) == 24:
            self.board_size = 'small'
        elif len(self.board.values()) == 32:
            self.board_size = 'large'
    
    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        self.num_turns += 1
        return self.minimax(self.board)
    
    def minimax(self, game_state):
         moves = game_state.get_all_available_legal_moves(self.our_color)
         best_move = moves[0]
         best_score = -1.0
         for move in moves:
             clone_state = copy.deepcopy(game_state)
             self.old_loc = move[0]
             self.new_loc = move[1]
             score = self.evaluate(clone_state)
             if self.old_loc == self.last_move:
                 score = -1.0
             this_score = score
             if self.board_size == 'small':
                 if self.num_turns >= 15:
                     clone_state.make_move(self.old_loc, self.new_loc)
                     if clone_state.is_king_in_check(self.their_color) == False and len(clone_state.get_all_available_legal_moves(self.their_color)) == 0:
                         score = -1.0
                     else:
                         score = this_score
             elif self.board_size == 'large':
                 if self.num_turns >= 25:
                     clone_state.make_move(self.old_loc, self.new_loc)
                     if clone_state.is_king_in_check(self.their_color) == False and len(clone_state.get_all_available_legal_moves(self.their_color)) == 0:
                         score = -1.0
                     else:
                         score = this_score
                 else:
                     if (self.new_loc[1] == '3' and game_state[self.old_loc].get_notation() == 'P') or (self.new_loc[1] == '6' and game_state[self.old_loc].get_notation() == 'p'):
                         score = -1.0
                     else:
                         score = this_score
             if score > best_score:
                 best_move = move
                 best_score = score
         self.last_move = best_move[1]
         return best_move
    
    def how_close_to_king(self, game_state):
         our_col = self.new_loc[0]
         our_row = int(self.new_loc[1])
         king_col = game_state.get_king_location(self.their_color)[0]
         king_row = int(game_state.get_king_location(self.their_color)[1])
         col_diff = abs(ord(our_col) - ord(king_col))
         row_diff = abs(our_row - king_row)
         if self.our_color == 'white' and game_state[self.old_loc].get_notation() == 'P' and self.new_loc[1] == '8':
             score = 10.0
         elif self.our_color == 'black' and game_state[self.old_loc].get_notation() == 'p' and self.new_loc[1] == '1':
             score = 10.0
         elif self.new_loc in game_state.keys():
             score = 1.0
         else:
             if col_diff == 1 or row_diff == 1 or (row_diff == 1 and col_diff == 1):
                 score = 0.0
             else:
                 score = (15 - (col_diff + row_diff))/15
         return score
    
    def evaluate(self, game_state):
        if self.board_size == 'small':
            if self.num_turns <= 15:
                if self.new_loc in game_state.keys():
                    piece = game_state[self.new_loc].get_notation()
                    score = self.piece_values[piece]
                else:
                    score = 0.0
            else:
                score = self.how_close_to_king(game_state)
        else:
            if self.num_turns <= 25:
                if self.new_loc in game_state.keys():
                    piece = game_state[self.new_loc].get_notation()
                    score = self.piece_values[piece]
                else:
                    score = 0.0
            else:
                score = self.how_close_to_king(game_state)
        return score
        