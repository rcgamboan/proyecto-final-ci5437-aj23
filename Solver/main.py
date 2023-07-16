from gen import *
from board import *
import sys

if __name__ == '__main__':

    # se llama con python3 main.py <archivo>
    # se asume que el archivo tiene el formato correcto
    # se asume que el archivo tiene al menos una fila y una columna
    
    # luego se crea un objeto Board con el archivo y se imprime
    # al crear el objeto se leera del archivo y se agregaran los datos a la matriz correspondiente
    tablero = Board(sys.argv[1])
    solver = SatSolver(tablero)

    # La solucion retornar una lista de la clase cells con la asignacion de cada
    # valor a cada celda
    tablero.print_board()
    cells = solver.solve()
    
    tablero.set_solution(cells)
    tablero.generate_board_img()
    
    print("Se ha generado la imagen kakuro_board.png con la solucion del problema!")
    print(cells)
