class Board(object):

    # se crea un objeto Board con el archivo suministrado
    # el tablero se representa como una matriz de listas
    # cada fila es una lista de listas donde [] representa una celda en blanco
    # y [x,y] representa una celda con un numero x y un numero y
    # si x o y son 0 entonces ese lado de la celda no tiene numero
    # ej: [0,0] representa una celda gris sin ningun numero
    #     [0,2] representa una celda gris con el numero 2 en la parte derecha
    #     [1,0] representa una celda gris con el numero 1 en la parte izquierda
    #     [1,2] representa una celda gris con el numero 1 en la parte izquierda y el numero 2 en la parte derecha    
    def __init__(self,file) -> None:
        self.row = 0
        self.col = 0
        self.board = []
        self.get_board(file)
    
    def add_row(self, row):
        self.board.append(row)

    def is_blank(self, row, col):
        if row < 0 or row >= self.row or col < 0 or col >= self.col:
            # fuera de limites
            return False
        return self.board[row][col] == []

    def get_columns(self):
        return self.col
    
    def get_rows(self):
        return self.row

    def print_board(self):
        for row in self.board:
            print(row)
    
    def get_cell(self, row, col):
        if row < 0 or row >= self.row or col < 0 or col >= self.col:
            # fuera de limites
            return None
        
        return self.board[row][col]


    def get_board(self,file):

        with open(file) as file:

            info = file.readline().split(" ")
            filas = int(info[0])
            columnas = int(info[1])

            for line in file:
                
                linea = line.rstrip("\n")
                elems = linea.split(" ")
                
                celdas = []
                
                for cell in elems:

                    if cell == '_':
                        celdas.append([])

                    elif cell[0] == '\\':

                        #print(f'cell : {cell}')
                        if len(cell) == 1:
                            celdas.append([0,0])
                        else:
                            s = cell.split("\\")
                            #print(f's : {s}')
                            celdas.append([0,int(s[1])])
                            
                    elif cell[0] != '\\':
                        
                        #print(f'cell : {cell}')
                        s = cell.split("\\")
                        try:
                            s.remove('')
                        except:
                            pass

                        #print(f's : {s}')
                        if len(s) > 1:
                            celdas.append([int(s[0]),int(s[1])])
                        else:
                            celdas.append([int(s[0]),0])

                #print(f'celdas : {celdas}')

                #self.add_row(elems)
                self.add_row(celdas)
        
        self.row = filas
        self.col = columnas
