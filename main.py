import random
import string
import time

from os import system, name

from player import Player
from board import Board
from utils import is_ans_in_list

def main():
        
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

        gamemode = str(input("Which gamemode would you like to play? [default/custom]" + "\n")).lower()
        msg = 'Sorry, I do not have that in my repertoire, please type in the preferred gamemode again.'
        gamemode = is_ans_in_list(answer=gamemode, ans_list=current_gamemodes, message=msg)



        if gamemode == 'default':
                player_count = 2
                board_size = 10

        elif gamemode == 'custom':
                player_count = input('How many players are playing today?' + '\n') 
                board_size =  input('How big should be the board?' + '\n')

        players_list = []
        for i in range(int(player_count)):
                print('\n'+'Player {i}, please enter your name :)'.format(i=i+1) + '\n')
                players_list.append(Player(board_class=Board, size=int(board_size)))
                print()
        # players_list = [Player(size=int(board_size)) for i in range(int(player_count))]

        adding_ships = str(input('\n'+'Now, would you like to add some ships? [yes/no]' +'\n')).lower()
        yes_no = ['yes', 'no']
        msg = 'Sorry, I did not understand that. Can you answer again?'
        adding_ships = is_ans_in_list(answer=adding_ships, ans_list=yes_no, message=msg)


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

                        keep_adding = is_ans_in_list(answer=keep_adding, ans_list=yes_no, message=msg) # same msg as before
                        


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
                
                print("""
        Possible moves include:

        ° attack -> attack enemy board
        ° stats -> current player statistics
        ° ships -> shows the fleet game started with

Please remember, that you MUST attack during each turn. Other options can be used,
but game will not progress unless you use your attack move.
                """)
                player_move = str(input('\n'+'What would you like to do first?' +'\n')).lower()

                player_move = is_ans_in_list(answer=player_move, ans_list=allowed_moves, message=msg) # same msg as before
               
                
                while player_move != 'attack':

                        if player_move == 'stats':
                                player.show_stats()
                        elif player_move == 'ships':
                                player.show_ships()

                        player_move = str(input('\n'+'What would you like to do now?' +'\n')).lower()

                        player_move = is_ans_in_list(answer=player_move, ans_list=allowed_moves, message=msg)
                       
                player_hit = True

                while player_hit:

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
                        print("LEGEND: X -> HIT BLOCK, S -> SHIP BLOCK, M -> MISSED BLOCK" + '\n')
                        player_hit = player.player_attack(opponent_board=opponent.board)  # opponent_board = Player.board
                        time.sleep(2) # delaying by 2 so that the player sees there was a hit
                        new_match = ''
                        # checking the winning condition        
                        if player.hits == player.winning_condition:
                                player.wins += 1
                                opponent.losses += 1
                                player_hit = False
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

                                new_match = str(input('\n' + 'Now, would like a rematch? [yes/no]' +'\n')).lower()

                                if new_match not in yes_no:
                                        new_match = is_ans_in_list(answer=new_match, ans_list=yes_no, message=msg)
                                        # while True:
                                        #         print("\n"+'Sorry, I did not understand that. Can you answer again?')
                                        #         new_match = str(input('\n'+'Would like a rematch? [yes/no]' +'\n')).lower()
                                        #         if new_match not in yes_no:
                                        #                 continue
                                        #         else:
                                        #                 break
                                if new_match == 'yes':
                                        # resetting player boards and hits/misses
                                        for player in players_list:
                                                player.reset_boards_and_stats()
                                                player.randomised_gamemode()
                                elif new_match == 'no':
                                        game_ended = True
                
                # incrementing for next player and waiting for player change
                if new_match != 'no':
                        wait_time = 5
                        print('\n' + 'Now you have {wait_time} seconds to swap places!'.format(wait_time=wait_time))
                        player.board.countdown(wait_time)



if __name__ == '__main__':
        main()