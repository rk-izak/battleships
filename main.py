import random
import string
import time

from os import system, name



class Board: # each player has one
        # 1->10 // A-->J
        def __init__(self, size=10): # size can be maximally 25, but 10 is preferred
                self.size = size
                self.alphabet = list(string.ascii_uppercase)[0:self.size]
                self.numbers = list(range(len(self.alphabet)))[0:self.size]
                # now turning lists to dicts
                self.alphabet = {self.alphabet[i]:i for i in range(self.size)}
                self.numbers = {str(self.numbers[i]+1):i for i in range(self.size)}

                self.board_matrix = [[' ' for i in range(len(self.numbers.keys()))] for j in range(len(self.alphabet))]

        def reset_board(self):
                self.board_matrix = [[' ' for i in range(len(self.numbers.keys()))] for j in range(len(self.alphabet))]
        
        def print_board(self):
                value_block = "|  "
                mark_line = '----' * (self.size+1)
                alphabet_line = "   ".join(self.alphabet.keys())
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
        def clear(self):
                # for windows
                if name == 'nt':
                        _ = system('cls')
                
                # for mac and linux(here, os.name is 'posix')
                else:
                        _ = system('clear')

        def countdown(self, t):
                while t:
                        mins, secs = divmod(t, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        t -= 1
            
# player class starts here

class Player:
        def __init__(self, size=10):
                # TODO: add different game settings for different board sizes 
                # i.e.: more ships, longer ships, etc.
                self.name = input('Chosen name: ')
                self.size = size
                self.ships ={"Carrier": (1,5), "Battleship":(1,4), "Cruiser": (1,3), 
                             "Destroyer": (2,2), "Subarmine": (2,1)} # "Name" : (count,length)
                self.winning_condition = sum([entry[0]*entry[1] for entry in self.ships.values()])
                self.wins = 0
                self.losses = 0
                self.hits = 0
                self.misses = 0
                self.board = Board(self.size)
                self.checking_board = Board(self.size)

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
                        print('!!! HIT !!!')
                        self.hits += 1
                        self.checking_board.board_matrix[column_pick][row_pick] = 'X'
                        opponent_board.board_matrix[column_pick][row_pick] = 'X'
                        # mark X on ur checking board and X on enemy game board
                else:
                        print('!!! MISS !!!')
                        self.misses += 1
                        self.checking_board.board_matrix[column_pick][row_pick] = 'M'
                        # mark M on ur checking board and do nothing on enemy boards
                        
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



# winning condition is basically if player.hits == player.winning_condition:
# player wins; else: another player takes their turn
# stats is bascially hits/misses/global wins that are stored in a txt file :)


print("""
============================================================================

    ____   ___   ______ ______ __     ______ _____  __  __ ____ ____  _____
   / __ ) /   | /_  __//_  __// /    / ____// ___/ / / / //  _// __ \/ ___/
  / __  |/ /| |  / /    / /  / /    / __/   \__ \ / /_/ / / / / /_/ /\__ \ 
 / /_/ // ___ | / /    / /  / /___ / /___  ___/ // __  /_/ / / ____/___/ / 
/_____//_/  |_|/_/    /_/  /_____//_____/ /____//_/ /_//___//_/    /____/  

============================================================================

        Welcome to the Command Line Game version of Battleships!

    
""")
print("First, please input which version of the below gamemodes you'd like to play today!")

print("""
DEFAULT: 

° players count -> 2
° board size -> 10x10
° basic ship set [name (length/count)]-> 
       * Carrier (5/1)
       * Battleship (4,1) 
       * Cruiser (3,1)
       * Destroyer (2,2)
       * Subarmine (1,2)
       + additional custom ships can be added

Additionally, all ships positions are randomised.


CUSTOM: 

° players count -> unlimited
° board size -> up to 25x25
° basic ship set [name (length/count)]-> 
       * Carrier (5/1)
       * Battleship (4,1) 
       * Cruiser (3,1)
       * Destroyer (2,2)
       * Subarmine (1,2)
        + additional custom ships can be added
Additionally, all ships positions can randomised or picked by each player [WIP: currently only randomised].

WARNING!!! The CUSTOM gamemode is a Work In Progress, therefore some bugs and unexpected behaviours might be encountered.
If you spot anything you think is wrong, please send me a message at: radoslawizak@gmail.com or make a Pull Request!

""")
current_gamemodes = ['default', 'custom']

gamemode = str(input("Which gamemode would you like to play?" + "\n")).lower()

if gamemode not in current_gamemodes:
        while True:
                print("\n"+'Sorry, I do not have that in my repertoire, please type in the preferred gamemode again.')
                gamemode = str(input("Which gamemode would you like to play?" + "\n")).lower()
                if gamemode not in current_gamemodes:
                        continue
                else:
                        break

if gamemode == 'default':
        player_count = 2
        board_size = 10

elif gamemode == 'custom':
        player_count = input('How many players are playing today?' + '\n') 
        board_size =  input('How big should be the board?' + '\n')

players_list = []
for i in range(int(player_count)):
        print('\n'+'Player {i}, please enter your name :)'.format(i=i+1) + '\n')
        players_list.append(Player(size=int(board_size)))
        print()
# players_list = [Player(size=int(board_size)) for i in range(int(player_count))]

adding_ships = str(input('\n'+'Now, would you like to add some ships? [yes/no]' +'\n')).lower()
yes_no = ['yes', 'no']

if adding_ships not in yes_no:
        while True:
                print("\n"+'Sorry, I did not understand that. Can you answer again?')
                adding_ships = str(input('\n'+'Would you like to add some ships? [yes/no]' +'\n')).lower()
                if adding_ships not in yes_no:
                        continue
                else:
                        break

if adding_ships == 'yes':
        keep_adding = True
        while keep_adding:
                players_list[0].add_ship()
                # now making sure that each player has also added that ship
                for player in players_list:
                        player.ships = players_list[0].ships
                        player.sort_ships_by_length()
                        player.update_winning_condition()
                keep_adding = str(input('\n' + 'Would you like to keep adding ships? [yes/no]' + '\n')).lower()
                if keep_adding not in yes_no:
                        while True:
                                print("\n"+'Sorry, I did not understand that. Can you answer again?')
                                keep_adding = str(input('\n'+'Would you like to stop adding ships? [yes/no]' +'\n')).lower()
                                if keep_adding not in yes_no:
                                        continue
                                else:
                                        break

                if keep_adding == 'no':
                        keep_adding = False

elif adding_ships == 'no':
        print('\n'+'No ships added, playing with the default ship set!' + '\n')
 
print('Please wait a second, the system is currently building the game!')
time.sleep(7) # setting it to 7s so that players can see what happened before + maybe later query time 

# setting all players boards
for player in players_list:
        player.randomised_gamemode()

# the playing section starts here
# initalizing and setting later used variables
game_ended = False
allowed_moves =['attack', 'stats', 'ships']
turn = 0

while not game_ended:
        # setting current player and opponent
        player = players_list[turn]
        if turn == (len(players_list) - 1):
                opponent = players_list[0]
                turn = 0
        else:
                opponent = players_list[turn+1]
                turn += 1
        # clearing command line to prevent cheating 
        player.board.clear()
        print('\n' + "NOW IT IS PLAYER'S {name} TURN!".format(name=player.name.upper()) + '\n')
        
        print("""Possible moves include:

        ° attack -> attack enemy board
        ° stats -> current player statistics
        ° ships -> shows the fleet game started with

        Please remember, that you MUST attack during each turn. Other options can be used,
        but game will not progress unless you use your attack move.
        """)
        player_move = str(input('\n'+'What would you like to do first?' +'\n')).lower()

        # making sure player move is in allowed moves
        if player_move not in allowed_moves:
                while True:
                        print("\n"+'Sorry, I did not understand that. Can you answer again?')
                        player_move = str(input('\n'+'What would you like to do?' +'\n')).lower()
                        if player_move not in allowed_moves:
                                continue
                        else:
                                break
        
        while player_move != 'attack':
        # if player_move == 'attack':
        #         player.player_attack(opponent_board=None)  # opponent_board = Player.board
                if player_move == 'stats':
                        player.show_stats()
                elif player_move == 'ships':
                        player.show_ships()

                player_move = str(input('\n'+'What would you like to do now?' +'\n')).lower()

                if player_move not in allowed_moves:
                        while True:
                                print("\n"+'Sorry, I did not understand that. Can you answer again?')
                                player_move = str(input('\n'+'What would you like to do?' +'\n')).lower()
                                if player_move not in allowed_moves:
                                        continue
                                else:
                                        break
        # once player did all they wanted, print boards again and attack
        print("""
 __        ___  __               __      __   __        __   __  
/  ` |__| |__  /  ` |__/ | |\ | / _`    |__) /  \  /\  |__) |  \ 
\__, |  | |___ \__, |  \ | | \| \__>    |__) \__/ /~~\ |  \ |__/                                             
        """)
        print()
        player.checking_board.print_board()
        print("""
     __        __      __   __        __   __  
\ / /  \ |  | |__)    |__) /  \  /\  |__) |  \ 
 |  \__/ \__/ |  \    |__) \__/ /~~\ |  \ |__/ 
        """)
        print()
        player.board.print_board()
        player.player_attack(opponent_board=opponent.board)  # opponent_board = Player.board

        # checking the winning condition        
        if player.hits == player.winning_condition:
                player.wins += 1
                opponent.losses += 1
                print("""
===============================================================

██    ██ ██  ██████ ████████  ██████  ██████  ██    ██ ██ ██ ██ 
██    ██ ██ ██         ██    ██    ██ ██   ██  ██  ██  ██ ██ ██ 
██    ██ ██ ██         ██    ██    ██ ██████    ████   ██ ██ ██ 
██  ██   ██ ██         ██    ██    ██ ██   ██    ██             
████     ██  ██████    ██     ██████  ██   ██    ██    ██ ██ ██ 

===============================================================
                """)
                print('\n' + 'Congratulations {name}! You have proven to be the better admiral!'.format(name=player.name))
                print('\n' + 'Hopefully, {op_name} will not take it personally ;) Good Game!'.format(op_name = opponent.name))

                new_match = str(input('\n' + 'Now, would like a rematch? [yes/no]')).lower()

                if new_match not in yes_no:
                        while True:
                                print("\n"+'Sorry, I did not understand that. Can you answer again?')
                                new_match = str(input('\n'+'Would like a rematch? [yes/no]' +'\n')).lower()
                                if new_match not in yes_no:
                                        continue
                                else:
                                        break
                if new_match == 'yes':
                        # resetting player boards and hits/misses
                        for player in players_list:
                                player.hits = 0
                                player.misses = 0
                                player.board.reset_board()
                                player.checking_board.reset_board()
                                player.randomised_gamemode()
                elif new_match == 'no':
                        game_ended = True
        
        # incrementing for next player and waiting for player change
        wait_time = 5
        print('\n' + 'Now you have {wait_time} seconds to swap places!'.format(wait_time=wait_time))
        player.board.countdown(wait_time)