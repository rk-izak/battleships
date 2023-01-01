import string
import random
alphabet = list(string.ascii_uppercase)


class Board: # each player has one
        # 1->10 // A-->J
        def __init__(self, size=10): # size can be maximally 25, but 10 is preferred
                self.size = size
                self.alphabet = list(string.ascii_uppercase)[0:self.size]
                self.numbers = list(range(len(self.alphabet)))[0:self.size]
                self.board_matrix = [[' ' for i in range(len(self.numbers))] for j in range(len(self.alphabet))]

        def print_board(self):
                value_block = "|  "
                mark_line = '----' * (self.size+1)
                alphabet_line = "   ".join(self.alphabet)
                print("    " + alphabet_line)
                print(mark_line[:-1])
                i = 1
                for row in self.board_matrix:
                        row_representation = ''.join([value_block[0:2] + str(entry) + value_block[-1] for entry in row])
                        if i < 10:
                                print(('0'+str(i) + row_representation + "|"))
                        else:
                                print((str(i) + row_representation + "|"))
                        print(mark_line[:-1])
                        i += 1
            
# player class starts here

class Player:
        def __init__(self, size=10):
                # TODO: add different game settings for different board sizes 
                # i.e.: more ships, longer ships, etc.
                self.size = size
                self.ships ={'Carriers': (1,5), "Battleships":(1,4), "Cruisers": (1,3), 
                             "Destroyers": (2,2), "Subarmines": (2,1)} # "Name" : (count,length)
                self.hits = 0
                self.winning_condition = sum([entry[0]*entry[1] for entry in self.ships.values()])
                self.misses = 0

        def picker_gamemode(self): # this is where all ships are odd and player can pick H/V and ships middle position
                pass

        def random_gamemode(self, board): # this is when all ships are spread randomly

                board = board(self.size)
                board_matrix = board.board_matrix
                board_row = board_matrix[0]
                # checking all possible horizontal position for all ships
                ship_position_indices = {k:[] for k in self.ships.keys()} # for any row or column

                for ship in self.ships.items():
                        name = ship[0]
                        length = ship[1][1]
                        index_pairs = [(i,i+length-1) for i in range(len(board_row) - length + 1)]
                        ship_position_indices[name] = (index_pairs)
                
                # picking positions starts here:
                for ship in self.ships.items():
                        name = ship[0]
                        count = ship[1][0]

                        for i in range(count):
                                unfinished_placing = True

                                while unfinished_placing:
                                        vertical_or_horizontal = random.choice([True, False]) # vertical if True, horizontal otherwise
                                        indices = random.choice(ship_position_indices[name])
                                        indices = list(range(indices[0], indices[1]+1))
                                        column_or_row =  random.randint(0, self.size-1) # random row or column

                                        found_duplicate = self.check_if_overlaps(vertical_or_horizontal=vertical_or_horizontal, 
                                        board_matrix=board_matrix, indices=indices, column_or_row=column_or_row)

                                        if found_duplicate:
                                                continue
                                        else:
                                                if vertical_or_horizontal: # if vertical
                                                        j = 0
                                                        for row in board_matrix:
                                                                if j in indices:
                                                                        row[column_or_row] = 'S'
                                                                j +=1
                                                else:
                                                        j = 0
                                                        for entry in board_matrix[column_or_row]:
                                                                if j in indices:
                                                                        board_matrix[column_or_row][j]='S'
                                                                j+=1
                                                unfinished_placing = False

        def check_if_filled(self, board_matrix, dict_items):
                count = 0
                actual = 0
                for value in dict_items:
                        actual += value[0]*value[1]
                for row in board_matrix:
                        count += row.count('S')
                if count == actual:
                        return True
                return False

        def check_if_overlaps(self, vertical_or_horizontal, board_matrix, indices, column_or_row):

                if vertical_or_horizontal: # if vertical
                        i = 0
                        for row in board_matrix:
                                if i in indices:
                                        if row[column_or_row] == 'S':
                                                return True
                                i+=1
                else:
                        i = 0
                        for entry in board_matrix[column_or_row]:
                                if i in indices:
                                        if board_matrix[column_or_row][i] == 'S':
                                                return True
                                i+=1
                return False


# player_1_board = Board()
# #player_1_board.print_board()
player = Player()
player.random_gamemode(Board)