# Written by Marcel Champagne, Student ID: 52532335, Lab Section 6, Assignment 5
import tkinter
import othello
import math
import time
import random

class OthelloGui:
    def __init__(self, game_state, ai):
        
        self._game_state = game_state
        self._ai = ai
        self._window = tkinter.Tk()
        self._window.title("Othello")
        self._window.rowconfigure(0, weight = 1)
        self._window.columnconfigure(0, weight = 1)

        self.settings()


    def run(self) -> None:
        self._window.mainloop()

    def start_othello(self) -> None:
        '''Sets up the othello GUI based on the game state.'''
        self._disc_width = 1/self._game_state.get_columns()
        self._disc_height = 1/self._game_state.get_rows()
        
        self._canvas = tkinter.Canvas(
            master = self._window,
            width = 100+self._game_state.get_columns()*75, height = self._game_state.get_rows()*75,
            background = '#18BA26')
        
        self._canvas.grid(
            row = 0, column = 0,
            sticky = tkinter.N + tkinter.E + tkinter.S + tkinter.W)
        
        self._canvas.bind('<Configure>', self.resize)
        self._canvas.bind('<Button-1>', self.update)

        self._ai_color = self._game_state.opposite_color(self._game_state.get_turn())

    def start_button(self) -> None:
        '''Checks all the input after the user clicks the 'start game' button.'''

        color_dict = {'BLACK':'B','WHITE':'W'}
        ai = self._entries['Computer AI'].get().upper()
        if ai == 'ON':
            self._ai = True
        rows = int(self._entries['Rows'].get())
        columns = int(self._entries['Columns'].get())
        top_left = color_dict[self._entries['Top-Left Color'].get().upper()]
        if top_left in ['W','B']:
            if top_left == 'W':
                colors = ['W','B']
            else:
                colors = ['B','W']
        first_move = color_dict[self._entries['First Move'].get().upper()]
        win_condition = self._entries['Win Condition'].get().upper().split()[0]
        
        self._game_state = othello.GameState(rows,columns,colors,first_move,win_condition)
        
        for key in self._entries:
            self._entries[key].grid_remove()
            self._labels[key].grid_remove()
            
        self._button.config(text = 'Restart')
        self.start_othello()

    def settings(self) -> None:
        '''Handles the settings widgets. Uses tkinter spinboxes for the interface.'''
        if self._game_state == None:
            self._title = tkinter.Label(master = self._window, text = 'Othello Settings', font = ('Arial',26))
            self._title.grid(row=0,column=0)
            labels = ['Rows','Columns','First Move','Computer AI','Win Condition','Top-Left Color']
            self._entries = {}
            self._labels = {}
            row_num = 1
            for key in labels:
                row_num += 2
                self._labels[key] = tkinter.Label(master = self._window, text = key, font = ('Arial',16))
                self._labels[key].grid(row=row_num,column=0,sticky = tkinter.N + tkinter.S + tkinter.W)

                if key in ['Rows','Columns']:
                    self._entries[key] = tkinter.Spinbox(master = self._window, values = ('8','10','12','14','16','4','6'), wrap = True, state = 'readonly')
                elif key == 'First Move':
                    self._entries[key] = tkinter.Spinbox(master = self._window, values = ('Black','White'), wrap = True, state = 'readonly')
                elif key == 'Top-Left Color':
                    self._entries[key] = tkinter.Spinbox(master = self._window, values = ('White','Black'), wrap = True, state = 'readonly')
                elif key == 'Win Condition':
                    self._entries[key] = tkinter.Spinbox(master = self._window, values = ('Most Pieces','Least Pieces'), wrap = True, state = 'readonly')
                elif key == 'Computer AI':
                    self._entries[key] = tkinter.Spinbox(master = self._window, values = ('Off','On'), wrap = True, state = 'readonly')

                self._entries[key].grid(row=row_num+1,column=0,sticky = tkinter.N + tkinter.E + tkinter.S + tkinter.W)
                
            self._button = tkinter.Button(master = self._window, text = 'Start Game', font = ('Arial',16), command = self.start_button)
            self._button.grid(row=row_num+2,column=0)
            
        else:
            self.start_othello()

    def resize(self, event: tkinter.Event) -> None:
        '''Called when the board is resized, calls the draw_board() event.'''
        self.draw_board()

    def update(self, event: tkinter.Event) -> None:
        '''Called when the mouse is clicked. Calculates where to place a piece.'''
        disc_column = math.floor((event.x-100)/(self._canvas.winfo_width()-100)*self._game_state.get_columns())
        disc_row = math.floor((event.y)/self._canvas.winfo_height()*self._game_state.get_rows())

        
        try:
            turn = self._game_state.get_turn()
            self._game_state.take_turn(turn,disc_row,disc_column)
        except:
            pass
        else:
            self.draw_board()

            #AI was added for fun -- I am aware that it is not part of this project
            #Nor should it be part of the GUI
            
            if self._ai == True:
                turn = self._game_state.get_turn()
                if turn == self._ai_color:
                    while turn == self._game_state.get_turn():
                        move_row,move_column = self._game_state.most_flipped(self._game_state.get_turn())
                        try:
                            self._game_state.take_turn(self._game_state.get_turn(),move_row,move_column)
                        except othello.InvalidTurnGameOver:
                            break
                        self._canvas.update()
                        time.sleep(random.choice([1.25,1.5,2,1.75,1.15]))
                        self.draw_board()
            
            

    def draw_board(self) -> None:
        '''Draws the othello board.'''
        # Clears the canvas
        self._canvas.delete(tkinter.ALL)
        board_width = self._canvas.winfo_width()-100
        board_height = self._canvas.winfo_height()

        colors = {'W':'white','B':'black'}

        # Gui
        font_size = math.floor(.036*board_height)
        turn = self._game_state.get_turn()
        if self._game_state.get_colors() == ['W','B']:
            black,white = self._game_state.count_pieces()
        else:
            white,black = self._game_state.count_pieces()
        display_pieces = True
        if font_size < 10:
            display_pieces = False
            font_size = 16
        elif font_size > 23:
            font_size = 23
            
        self._canvas.create_rectangle(0, 0, 100, board_height, fill = '#E8BA2E')
        self._canvas.create_line(100, 0, 100, board_height, width = 6, fill = '#1A2919')
        
        if self._game_state.is_game_over() == False:
            self._canvas.create_text(5, 1*(board_height*.2), text = 'Turn:\n'+colors[turn].capitalize(), font=("Times",font_size),anchor=tkinter.NW)
        else:
            winner = self._game_state.get_winner()
            if winner != None:
                self._canvas.create_text(5, 1*(board_height*.2), text = 'Winner:\n'+colors[winner].capitalize(), font=("Times",font_size),anchor=tkinter.NW)
            else:
                self._canvas.create_text(5, 1*(board_height*.2), text = 'Tie!', font=("Purisa",font_size),anchor=tkinter.NW)
        if display_pieces:
            self._canvas.create_text(5, 2*(board_height*.2), text = 'White:\n'+str(black), font=("Times",font_size),anchor=tkinter.NW)
            self._canvas.create_text(5, 3*(board_height*.2), text = 'Black:\n'+str(white), font=("Times",font_size),anchor=tkinter.NW)

        #Draw the discs
        row_num = 0
        for board_row in self._game_state.get_board():
            column_num = 0
            for piece in board_row:
                if column_num > 0:
                
                    self._canvas.create_line(100+column_num * (self._disc_width * board_width), 0,
                                             100+column_num * (self._disc_width * board_width), board_height, width = 3, fill = '#043008')
                if row_num > 0:
                    self._canvas.create_line(100, row_num * (self._disc_height * board_height),
                                             board_width+100, row_num * (self._disc_height * board_height), width = 3, fill = '#043008')
                if piece != None:

                    self._canvas.create_oval(100+column_num * (self._disc_width * board_width)+(.007*board_height),
                                             row_num * (self._disc_height * board_height)+(.007*board_width),
                                             100+(column_num+1) * (self._disc_width * board_width)-(.007*board_height),
                                             (row_num+1) * (self._disc_height * board_height)-(.007*board_width),
                                             fill = colors[piece],
                                             outline = colors[self._game_state.opposite_color(piece)],
                                             activeoutline = 'yellow')
                column_num += 1
            row_num += 1

def main() -> None:
    '''Starts the program.'''
    gui = OthelloGui(None,False)
    gui.run()    

if __name__ == '__main__':
    main()
