from os import system, name
import string
import time

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