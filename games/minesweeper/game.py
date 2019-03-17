import numpy as np 
import random
import math 
positions = [[0,1],[1,0],[1,1],[-1,0],[0,-1],[-1,-1],[1,-1],[-1,1]]

class Game:
    def __init__(self,x,y, n_bombs):
        self.state = 'Pending'
        self.x =x 
        self.y = y

        self.n_bombs = n_bombs
        self.game_board = Board(self.x,self.y, n_bombs)

    def reset(self):
        del self.game_board
        self.game_board = Board(self.x,self.y)

    def click(self,x,y, to_flag = 0):
        if to_flag:
            if self.game_board.is_open(x,y):
                return None
            self.game_board.flag(x,y)
            return self.game_board.Tiles[x,y].flag

        if self.game_board.has_bomb(x,y):
            if self.get_tile_state(x,y) == 0:
                # Trying to click on a tile with flag
                return None
            self.state = 'Lost'
            return -1 
        else:
            if not self.game_board.Tiles[x,y].open and not self.game_board.Tiles[x,y].flag:
                self.game_board.Tiles[x,y].open = True

                return self.game_board.get_near_bombs(x,y)
            return None

    def click_around(self,position):
        """ 
        to_open : [x,y,bomb]

        """
        x,y = position 
        new_pos = []
        to_open = []
        for pos in positions:
            try:

                if x - pos[0] >=0 and y -pos[1] >=0 :
                    if self.game_board.is_open(x - pos[0] ,y -pos[1] ):
                        # already open 
                        continue
                    bombs = self.click(x-pos[0],y-pos[1])

                    to_open.append([x-pos[0], y-pos[1], bombs])

                    if bombs == 0:
                        new_pos.append([x-pos[0], y-pos[1]])
            except Exception as e:
                print(e)
                pass
        return new_pos, to_open


    def get_tile_state(self,x,y):

        tile = self.game_board.Tiles[x,y]
        if tile.has_flag:
            return 0
        elif tile.open:
            return 1

    @property
    def is_over(self):
        result = self.game_board.is_finished
        if result:
            self.state = 'Won'
        
        return self.state != 'Pending'
    
class Board:
    def __init__(self, size_x,size_y, n_bombs):
        self.Tiles = np.empty( (size_x,size_y), dtype=object)
        self.size_x = size_x
        self.size_y = size_y
        for j in range(size_x):
            for i in range(size_y):
                self.Tiles[j,i] = Tile()
        self.n_bombs = n_bombs

        result = self.place_random_bombs()

        if result != 0:
            print("No bombs were placed. Problem with number of bombs")
        self.calculate_near_bombs()
        self.revealed = 0
        self.have_flag = 0

        self.correct_flags = 0

    def calculate_near_bombs(self):
        for j in range(self.size_x):
            for i in range(self.size_y): 
                for pos in positions:
                    try:
                        if self.Tiles[j - pos[0],i-pos[1]]._bomb and j - pos[0] >=0 and i-pos[1] >=0:
                            self.Tiles[j,i].near_bombs +=1
                    except Exception as e:
                        pass
    def get_near_bombs(self,x,y):
        """
        Only called when the tile is clicked upon
        """
        self.revealed += 1
        return self.Tiles[x,y].near_bombs

    def has_bomb(self,x,y):
        return self.Tiles[x,y]._bomb

    def flag(self,x,y):
        flag_val = self.Tiles[x,y].change_flag()

        if flag_val and self.Tiles[x,y].has_bomb:
            self.correct_flags += 1
        elif not flag_val and self.Tiles[x,y].has_bomb:
            self.correct_flags -= 1
        if flag_val:
            self.have_flag += 1
        else:
            self.have_flag -= 1

    def is_open(self,x,y):
        return self.Tiles[x,y].open

    @property  
    def is_finished(self):
        n_tiles = self.size_x * self.size_y 
        if self.have_flag > self.n_bombs:
            return False

        if self.correct_flags  + self.revealed == n_tiles:
            return True
        elif self.revealed == n_tiles - self.n_bombs:
            return True
        elif self.correct_flags == self.n_bombs:
            return True
        else:
            return False

    def place_random_bombs(self, how_many = None):
        missing = 0
        n_tiles = self.size_x * self.size_y
        if how_many is None:
            how_many = self.n_bombs
        mylist = [(random.randint(0, self.size_x -1),random.randint(0, self.size_y-1) ) for k in range(how_many)]
        if self.n_bombs > 0.7*n_tiles:
            return -1
        for val in mylist:
            result = self.Tiles[val[0],val[1]].set_bomb()
            if result == -1:
                missing += 1

        if missing != 0:
            return self.place_random_bombs(how_many = missing)

        else:
            return 0

class Tile:
    def __init__(self):
        self._bomb = 0
        self.near_bombs = 0

        self.flag = False
        self.open = False 
    def __repr__(self):
        return f"{self._bomb}"

    def change_flag(self):
        self.flag = not self.flag
        return self.flag
    @property
    def has_flag(self):
        return self.flag
    @property
    def has_bomb(self):
        return self._bomb
    
    def set_bomb(self):
        if self._bomb != 0:
            return -1
        self._bomb = 1
        return 0
if __name__ == '__main__':
    x = Board(3,3,10)

    x = not False
    print(x)
