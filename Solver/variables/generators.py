def partition_min_max(n,k,l,m):
    'Consigue las k particiones posibles de un numero n'
    if k < 1:
        return
    if k == 1:
        if n <= m and n>=l :
            yield (n,)
        return
    if (k*128) < n: #If the current sum is too small to reach n
        return
    if k*1 > n:#If current sum is too big to reach n
        return
    for i in range(l,m+1):
        for result in partition_min_max(n-i,k-1,i,m):                
            yield result+(i,)

def has_duplicates(list):
    prev_len = len(list)
    a_set = set(list)
    return prev_len != len(a_set)

def generate_partitions(n,k,m,l=1):

    y = [x for x in partition_min_max(n, k, l, m)]
    z = list(filter(lambda x: not has_duplicates(x), y))
    return z


class VarsGenerator():
    def __init__(self, board, values):
        self.total_rows = board.row
        self.total_cols = board.col
        self.total_values = values
        self.board = board
        self.len_total_rows = len(str(board.row))
        self.len_total_cols = len(str(board.col))

    def format(self, var, len):
        x =  "{:0" + str(len) + "}"
        return x.format(var)

    def format_row(self, team):
        return self.format(team, self.len_total_rows)

    def format_col(self, day):
        return self.format(day, self.len_total_cols)

    def format_var(self, row, col, value, auxiliar=''):
        assert len(str(row)) <= self.total_rows
        assert len(str(col)) <= self.total_cols
        return ''.join([
            self.format_row(row),
            self.format_col(col),
            auxiliar,
            str(value)
        ])

    def generate_variables(self):
        vars = []
        white_cells = []

        
        # Obtener las celdas donde deben ir los valores
        for row in range(0, self.total_rows):
            for col in range(0, self.total_cols):
                cell = self.board.get_cell(row, col)
                if cell != []:
                    continue
                white_cells.append((row+1, col+1))
                for value in range(1, self.total_values+1):
                    vars.append(
                        self.format_var(row+1, col+1, value)
                    )

        self.white_cells = white_cells        
        # Obtener las filas de celdas adjacentes
        adjacent_cells_rows = [[]]

        for cell in white_cells:
            last_added_row = adjacent_cells_rows[-1] 
            if len(last_added_row) == 0 or last_added_row[-1] == (cell[0], cell[1]-1):
                last_added_row.append(cell)
                
            else:                
                adjacent_cells_rows.append([cell])
        self.adjacent_cells_rows = adjacent_cells_rows

        # Obtener las columnas de celdas adjacentes
        adjacent_cells_cols = [[]]
        for col in range(0, self.total_rows):
            for row in range(0, self.total_cols):
                cell = self.board.get_cell(row, col)
                if cell != []:
                    continue
                cell = (row+1, col+1)
                last_added_col = adjacent_cells_cols[-1]
                if len(last_added_col) == 0 or last_added_col[-1] == (cell[0]-1, cell[1]):
                    last_added_col.append(cell)
                else:
                    adjacent_cells_cols.append([cell])
        self.adjacent_cells_cols = adjacent_cells_cols

        # Variables auxiliares. Columnas/Filas contiene al valor value
        for row in adjacent_cells_rows:
            (row, col) = row[0]
            for value in range(1, self.total_values+1):
                vars.append(
                    self.format_var(row, col, value, "fc")
                )

        for col in adjacent_cells_cols:
            (row, col) = col[0]
            for value in range(1, self.total_values+1):
                vars.append(
                    self.format_var(row, col, value, "cc")
                )
        
        # Variables auxiliares para la suma
        # Combinaciones de particiones de k numeros que suman un numero n
        for row in adjacent_cells_rows:
            # Obtener la suma objetivo de la fila
            objective_value = self.board.get_cell(row[0][0]-1, row[0][1]-2)[1]
            partitions = generate_partitions(objective_value, len(row), 9)
        
            for partition in partitions:
                vars.append(
                        self.format_var(row[0][0], row[0][1]-1, 0, str(partition))
                    )
        
        for col in adjacent_cells_cols:
            # Obtener la suma objetivo de la fila
            objective_value = self.board.get_cell(col[0][0]-2, col[0][1]-1)[0]
            partitions = generate_partitions(objective_value, len(col), 9)
            
            for partition in partitions:
                vars.append(
                        self.format_var(col[0][0], col[0][1]-1, 0, str(partition))
                    )

        return vars

    def generate_values_per_cell(self, row, col):
        vars = []
        for value in range(1, self.total_values+1):
            vars.append(self.format_var(row, col, value))
        return vars

    def generate_adjacent_cells_per_value(self, cells, value):
        vars = []
        for (row, col) in cells:
            vars.append(self.format_var(row, col, value))
        return vars
