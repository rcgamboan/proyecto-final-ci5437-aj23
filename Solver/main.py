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
    solver.solve()

