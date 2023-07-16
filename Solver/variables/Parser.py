class Parser():
    def __init__(self, vars, rows, cols, values):
        self.vars = vars
        self.rows = rows
        self.cols = cols
        self.values = values 
        
        self.len_rows = len(str(rows))
        self.len_cols = len(str(cols))
        self.values = len(str(values))
        

    def parse_vars(self):
        output = []
        for var in self.vars:
            try:
                value = int(var[self.len_rows+self.len_cols:])
            except ValueError:
                continue
            row = var[:self.len_rows]
            col = var[self.len_rows:self.len_rows+self.len_cols]
            

            output.append(
                Cell(row, col, value)
            )
        return output

class Cell():
    def __init__(self, row, col, value):
        self.row = int(row)
        self.col = int(col)
        self.value = int(value)

    def __repr__(self) -> str:
        return f"{(self.row,self.col)} : {self.value}"
        