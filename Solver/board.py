from PIL import Image, ImageDraw, ImageFont

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

    def set_solution(self, solution):
        pass
    
    def generate_board_img(self):

        # Define the size of each cell in pixels
        cell_size = 100

        # Calculate the board size
        width = len(self.col) * cell_size
        height = len(self.row) * cell_size

        # Create a blank image
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # Set the font properties
        font_size = cell_size // 2
        font = ImageFont.truetype("arial.ttf", font_size)
        split_font = ImageFont.truetype("arial.ttf", cell_size // 3)

        # Draw the Kakuro board
        for i in range(len(self.row)):
            for j in range(self.col):
                # Calculate the cell position
                x = j * cell_size
                y = i * cell_size

                # Draw the cell value
                cell = self.board[i][j]
                split_cell = False
                if len(cell) == 0:
                    cell_value = 0
                elif len(cell) == 2:
                    split_cell = True
                    cell_value = cell[0] + cell[1]

            
                # Draw the cell
                if len(cell) > 0:
                    draw.rectangle([(x, y), (x + cell_size, y + cell_size)], fill="gray", outline="black")
                else:
                    draw.rectangle([(x, y), (x + cell_size, y + cell_size)], fill="white", outline="black")
                

                if cell_value > 0:
                    text_width, text_height = draw.textsize(str(cell_value), font=font)
                    text_x = x + (cell_size - text_width) // 2
                    text_y = y + (cell_size - text_height) // 2

                    # Check if the cell should be split
                    if split_cell:
                        # Calculate the coordinates for the triangles
                        triangle_coords = [(x, y), (x + cell_size, y), (x + cell_size, y + cell_size), (x, y + cell_size)]

                        # Draw the upper triangle
                        draw.polygon(triangle_coords[:3], fill="gray", outline="black")

                        # Draw the cell value in the lower triangle
                        if cell[0] > 0:
                            draw.text((text_x, text_y + cell_size // 3), str(cell[0]), fill="black", font=split_font)

                        # Draw the cell value in the upper triangle
                        if cell[1] > 0:
                            draw.text((text_x+cell_size//2.5, text_y), str(cell[1]), fill="black", font=split_font)
                    else:
                        draw.text((text_x, text_y), str(cell_value), fill="black", font=font)

        # ...


        # Save the image
        image.save("kakuro_board.png")


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
