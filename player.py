import random

class Player:
        def __init__(self, board_class, size=10):
                # TODO: add different game settings for different board sizes 
                # i.e.: more ships, longer ships, etc.
                self.name = input('Chosen name: ')
                self.size = size
                # self.ships ={"Carrier": (1,5), "Battleship":(1,4), "Cruiser": (1,3), 
                #              "Destroyer": (2,2), "Subarmine": (2,1)} # "Name" : (count,length)
                self.ships = {"Subarmine": (1,1)}
                self.winning_condition = sum([entry[0]*entry[1] for entry in self.ships.values()])
                self.wins = 0
                self.losses = 0
                self.hits = 0
                self.misses = 0
                self.board = board_class(self.size)
                self.checking_board = board_class(self.size)

        def sort_ships_by_length(self):
                sorted_ships = dict(sorted(self.ships.items(), key=lambda x:x[1][1], reverse=True))
                self.ships = sorted_ships

        def add_ship(self):
                
                ship_name = input('Please, provide the new ship name: ') # this can be anything
                ship_count = self.input_positive_int('count')
                ship_length = self.input_positive_int('length')

                current_lengths = [value[1] for value in self.ships.values()]

                while ship_name in self.ships.keys() : # checking if the key/length already exists
                        print('Sorry, this name is already taken. Please, try again!')
                        ship_name = input('Please, provide the new ship name: ')

                while ship_length > self.size:
                        print('Sorry! The ship is too large for current board size! Try again!')
                        ship_length = self.input_positive_int('length')

                while ship_length in current_lengths:
                        print('Sorry! There already exists a ship with that length! Try again!')
                        ship_length = self.input_positive_int('length')
                # checking if the board will be completely filled after a ship is added:

                if self.winning_condition + (ship_count * ship_length) > 0.5 * self.size ** 2:
                        print('Sorry! The board would be too overfilled as it cannot be more than 60% full.')
                        ship_count = 0
                elif ship_length == 0:
                        print('The length of a ship cannot be 0! Skipping.')
                        ship_count = 0
                else:
                        self.ships[ship_name] = (ship_count, ship_length)
                
                print()
                if ship_count > 1:
                        print('The ships have been added!')
                elif ship_count == 0:
                        print('No ships have been added!')
                elif ship_count == 1:
                        print('The ship has been added!')

        def custom_gamemode(self): # this is where all ships are odd and player can pick H/V and ships middle position
                pass   

        def randomised_gamemode(self): # this is when all ships are spread randomly

                board_matrix = self.board.board_matrix
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
        def player_attack(self, opponent_board): # opponent_board = Player.board

                move = input('Please, input the move in the format of LETTER+NUMBER (for example, B2): ')
                letter_pick = move[0]
                number_pick = move[1:]

                while letter_pick.upper() not in self.board.alphabet.keys() or str(number_pick) not in self.board.numbers.keys():
                        if letter_pick.upper() not in self.board.alphabet:
                                print('Sorry! The letter has been input incorretly. Please, try again!')
                                move = input('Please, input the move in the format of LETTER+NUMBER (for example, B2): ')
                                letter_pick = move[0]
                                number_pick = move[1:]
                        else:
                                print('Sorry! The number has been input incorretly. Please, try again!')
                                move = input('Please, input the move in the format of LETTER+NUMBER (for example, B2): ')
                                letter_pick = move[0]
                                number_pick = move[1:]

                row_pick = self.board.alphabet[str(letter_pick).upper()]
                column_pick = self.board.numbers[str(number_pick)]
                
                # block_picked = self.board.board_matrix[column_pick][row_pick] # correctly picks currently for our board
                block_picked = opponent_board.board_matrix[column_pick][row_pick] 
                if str(block_picked) == 'S':
                        print('!!! HIT !!!' + '\n' + '!!!ATTACK AGAIN!!!')
                        self.hits += 1
                        self.checking_board.board_matrix[column_pick][row_pick] = 'X'
                        opponent_board.board_matrix[column_pick][row_pick] = 'X'
                        # mark X on ur checking board and X on enemy game board
                        return True
                else:
                        print('!!! MISS !!!' '\n' + '!!!CHANGING PLAYERS!!!')
                        self.misses += 1
                        self.checking_board.board_matrix[column_pick][row_pick] = 'M'
                        # mark M on ur checking board and do nothing on enemy boards
                        return False

        def reset_boards_and_stats(self):
                self.hits = 0
                self.misses = 0
                self.board.reset_board()
                self.checking_board.reset_board()

        def update_winning_condition(self):
                # updating winning condition
                self.winning_condition = sum([entry[0]*entry[1] for entry in self.ships.values()])

        def show_ships(self):
                print('\n' + 'The ships for this gamemode are as follows:' +'\n')
                for name in self.ships:
                        length = self.ships[name][1]
                        count = self.ships[name][0]
                        print("""
° Name: {name}
° Length: {length} 
° Count: {count}""".format(name=name, length=length, count=count))
                        

        def show_stats(self):
                print()
                print("""
The states for {name} are as follows:
° misses: {misses}
° hits: {hits}
° total wins: {wins}
° total losses: {losses}""".format(name=self.name, misses=self.misses, hits = self.hits, wins = self.wins, losses = self.losses))
                
        def check_if_filled(self, board_matrix, dict_values):
                count = 0
                actual = 0
                for value in dict_values:
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

        def input_positive_int(self, name):
                while True:
                        number = input("Enter the ship's {}: ".format(name))
                        try:
                                val = int(number)
                                if val < 0:  # if not a positive int print message and ask for input again
                                        print("Sorry, input must be a positive integer, try again!")
                                        continue
                                break
                        except ValueError:
                                print("Input must be an integer!")
                return val