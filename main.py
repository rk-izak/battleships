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

        
# ship classes start here:        
class Carrier: # length: 5 count: 1
        def __init__(self):
                self.length = 5
                self.hit = 0
class Battleship: # length: 4 count: 1
        def __init__(self):
                self.length = 4
                self.hit = 0
class Cruiser: # length: 3 count: 1
        def __init__(self):
                self.length = 3
                self.hit = 0
class Destroyer: # length: 2 count: 2
        def __init__(self):
                self.length = 2
                self.hit = 0
class Submarine: # length: 1 count: 2
        def __init__(self):
                self.length = 1
                self.hit = 0
                
player_1_board = Board()
player_1_board.print_board()