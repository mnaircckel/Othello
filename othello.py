# Written by Marcel Champagne, Student ID: 52532335, Lab Section 6, Assignment 5
class InvalidBoardSize(Exception):
    pass

class InvalidTurnColor(Exception):
    pass

class InvalidTurnLocation(Exception):
    pass

class InvalidTurnGameOver(Exception):
    pass

class InvalidTurnTileOccupied(Exception):
    pass

class InvalidWinCondition(Exception):
    pass

class InvalidTurnOffBoard(Exception):
    pass

class InvalidColors(Exception):
    pass

class InvalidFirstTurn(Exception):
    pass

class GameState:
    
    def __init__(self, rows: int, columns: int, colors: [str], turn: str, win_condition: str):
        self._rows = rows
        self._columns = columns
        self._colors = colors
        self._turn = turn
        self._win_condition = win_condition
        self._board = self.new_board()
        self._game_over = False

    def new_board(self) -> '2D list of strings':
        '''Creates an empty board with the intitial 4 pieces.'''
        board = []
        middle_row = (self._rows//2)-1
        middle_column = (self._columns//2)-1

        #Invalid Colors
        if self._colors not in [['W','B'],['B','W']]:
            raise InvalidColors

        #Invalid First Turn
        if self._turn not in ['W','B']:
            raise InvalidFirstTurn

        #Invalid Win Condition
        if self._win_condition not in ['MOST','LEAST']:
            raise InvalidWinCondition
        
        # Raise an exception if the board dimensions are too high or low
        if self._rows > 16 or self._rows < 4 or self._columns > 16 or self._columns < 4:
            raise InvalidBoardSize

        # Raise an exception if the board dimensions are not even
        if middle_row != (self._rows/2)-1 or middle_column != (self._columns/2)-1:
            raise InvalidBoardSize

        # Create a blank board
        for row in range(self._rows):
            board.append([])
            for piece in range(self._columns):
                board[row].append(None)

        # Create the initial 4 pieces
        board[middle_row][middle_column] = self._colors[0]
        board[middle_row+1][middle_column+1] = self._colors[0]
        board[middle_row][middle_column+1] = self._colors[1]
        board[middle_row+1][middle_column] = self._colors[1]
        
        return board

    def take_turn(self, color: str, row: int, column: int) -> None:
        '''The entire turn procress is broken up in this function. It also catches invalid turns.'''

        if color != self._turn:
            raise InvalidTurnColor

        if self._game_over == True:
            raise InvalidTurnGameOver

        if row < 0 or column < 0:
            raise InvalidTurnOffBoard
        
        try:
            if self._board[row][column] != None:
                raise InvalidTurnTileOccupied
        except IndexError:
            raise InvalidTurnOffBoard
        
        switch_tiles = self.tiles_to_flip(color, row, column)
        if len(switch_tiles) > 0 :
            
            self.place_piece(color, row, column)
            self.flip_tiles(switch_tiles)
            self.update_turn()
            
        else:
            raise InvalidTurnLocation

    def place_piece(self, color: str, row: int, column: int) -> None:
        '''Places a piece on the game board.'''
        self._board[row][column] = color

    def tiles_to_flip(self, color: str, row: int, column: int) -> '2D list of strings':
        ''' Determines the tiles to flip based on the color, row, and column. '''
        
        #              E     SE      S      SW      W       NW       N      NE  
        directions = [ [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1] ]
        tiles = []

        for direction in directions:

            tile_x = row
            tile_y = column
            tiles_to_add = []
            while True:
                tile_y += direction[0]
                tile_x += direction[1]
                
                if tile_x > self._rows-1 or tile_x < 0:
                    break
                if tile_y > self._columns-1 or tile_y < 0:
                    break

                if self._board[tile_x][tile_y] == self.opposite_color(color):
                    tiles_to_add.append([tile_x,tile_y])
                elif self._board[tile_x][tile_y] == color:
                    tiles.extend(tiles_to_add)
                    break
                else:
                    break
                
        return tiles

    def flip_tiles(self, tiles: '2D list of strings') -> None:
        ''' Flips tiles based on a list of given locations. '''
        for tile in tiles:
            self._board[tile[0]][tile[1]] = self.opposite_color(self._board[tile[0]][tile[1]])

    def opposite_color(self, color) -> str:
        ''' Returns the opposite color. '''
        if color == self._colors[0]:
            return self._colors[1]
        else:
            return self._colors[0]

    def update_turn(self) -> str or None:
        ''' Updates the turn by looking at the board and determining avaliable moves. '''
        if self.moves_avaliable(self.opposite_color(self._turn)):
            self._turn = self.opposite_color(self._turn)
        elif self.moves_avaliable(self._turn):
            pass
        else:
            self._game_over = True

    def moves_avaliable(self, color) -> int:
        ''' Determines avaliable moves based on color. '''
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == None:
                    if len(self.tiles_to_flip(color, row, column)) > 0:
                        return True
        return False

    def most_flipped(self, color) -> int:
        ''' Determines best move based on color. '''
        tiles = 0
        this_row,this_column = 0,0
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == None:
                    flipped = len(self.tiles_to_flip(color, row, column))
                    
                    if flipped > 0:

                        bad_locations = [ [1,1],[1,0],[0,1],         [self._rows-2,self._columns-2],[self._rows-1,self._columns-2],[self._rows-2,self._columns-1],         [1,self._columns-2],[0,self._columns-2],[1,self._columns-1],          [self._rows-2,1],[self._rows-1,1],[self._rows-2,0]  ]
                        
                        good_locations = [ [0,0],[self._rows-1,self._columns-1],[0,self._columns-1],[self._rows-1,0] ]                  
                                          
                        if [row,column] in bad_locations:
                            flipped = flipped-6
                            if flipped < 1:
                                flipped = .5

                        elif [row,column] in good_locations:
                            flipped = 20

                        elif row == 0 or column == 0 or row == self._rows-1 or column == self._columns-1:
                            flipped = flipped+4

                        elif row == 1 or column == 1 or row == self._rows-2 or column == self._columns-2:
                            flipped = flipped-3
                            if flipped < 1:
                                flipped = .5
                        
                    if  flipped > tiles:
                        tiles = flipped
                        this_row,this_column = row,column
                        
        return this_row,this_column

    def count_pieces(self) -> int and int:
        ''' Counts the number of pieces for both colors.'''
        color_one_pieces = 0
        color_two_pieces = 0
        
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == self._colors[0]:
                    color_one_pieces += 1
                elif self._board[row][column] == self._colors[1]:
                    color_two_pieces += 1
                
        return color_one_pieces,color_two_pieces

    def get_winner(self) -> str or None:
        '''Returns the winner based on win condition and pieces count.'''
        color_one,color_two = self.count_pieces()
        winner = None

        if color_one > color_two:
            winner = self._colors[0]
        elif color_one == color_two:
            winnter = None
        else:
            winner = self._colors[1]
            
        if self._win_condition == 'MOST':
            return winner
        elif self._win_condition == 'LEAST':
            return self.opposite_color(winner)
        else:
            raise InvalidWinCondition

    def get_turn(self) -> str:
        '''Returns current turn.'''
        return self._turn

    def get_colors(self) -> str:
        '''Returns colors.'''
        return self._colors

    def get_rows(self) -> int:
        '''Returns number of board rows.'''
        return self._rows

    def get_columns(self) -> int:
        '''Returns number of column rows.'''
        return self._columns

    def get_board(self) -> '2D list of strings':
        '''Returns the entire board.'''
        return self._board

    def is_game_over(self) -> bool:
        '''Returns if the game is over or not.'''
        return self._game_over
