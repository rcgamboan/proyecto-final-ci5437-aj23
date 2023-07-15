class Board(object):
    def __init__(self,file) -> None:
        self.row = 0
        self.col = 0
        self.board = []
        self.get_board(file)
    
    def add_row(self, row):
        self.board.append(row)

    def is_blank(self, row, col):
        if row < 0 or row >= self.row or col < 0 or col >= self.col:
            return False
        return self.board[row][col] == '_'

    def get_columns(self):
        return self.col
    
    def get_rows(self):
        return self.row

    def print_board(self):
        for row in self.board:
            print(row)

    def get_board(self,file):

        with open(file) as file:

            info = file.readline().split(" ")
            filas = int(info[0])
            columnas = int(info[1])

            for line in file:
                linea = line.rstrip("\n")
                elems = linea.split(" ")
                self.add_row(elems)
        
        self.row = filas
        self.col = columnas
