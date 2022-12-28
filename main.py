import string
alphabet = list(string.ascii_uppercase)


class Board: # each player has one
        # 1->10 // A-->J
        def __init__(self, size=10): # size can be maximally 25, but 10 is preferred
                self.size=size
                self.alphabet = list(string.ascii_uppercase)[0:self.size]
                self.numbers = list(range(len(self.alphabet)))[0:self.size]
                self.letter_rows = {v:k for (k,v) in enumerate(self.alphabet)}
                self.number_rows = {str(v+1):k for (k,v) in enumerate(self.numbers)}
                
        def print_board(self):
        
                value_block = "|   "
                mark_line = '----' * (self.size+1)
                alphabet_line = "   ".join(self.alphabet)
                print("    " + alphabet_line)
                print(mark_line)
                for number in self.number_rows:
                        if int(number) < 10:
                                print(('0'+number + value_block * len(self.letter_rows)) + "|")
                        else:
                                print((number + value_block * len(self.letter_rows)) + "|")
                        print(mark_line)
            
# player class starts here

class Player:
        def __init__(self, size=10):
                # TODO: add different game settings for different board sizes 
                # i.e.: more ships, longer ships, etc.
                self.size = size
                self.ships ={'Carriers': (1,5), "Battleships":(1,4), "Cruisers": (1,3), 
                             "Destroyers": (2,2), "Subarmines": (2,1)} # "Name" : (count,length)
                self.hits = 0
                self.misses = 0
                
        def create_board(self):
                pass
        
player_1_board = Board()
player_1_board.print_board()