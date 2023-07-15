from itertools import product
class VarsGenerator():
    def __init__(self, board):
        self.total_rows = board.row
        self.total_cols = board.col
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

    def format_var(self, row, col, value):
        assert len(str(row)) <= self.total_rows
        assert len(str(col)) <= self.total_cols
        return ''.join([
            self.format_row(row),
            self.format_col(col),
            str(value)
        ])

    def generate_variables(self):
        vars = []
        for row in range(0, self.total_rows):
            for col in range(0, self.total_cols):
                cell = self.board.get_cell(row, col)
                if cell != []:
                    continue
                for value in range(1, 10):
                    vars.append(
                        self.format_var(row+1, col+1, value)
                    )
        
        return vars


    # def generate_variables(self):
    #     vars = []
    #     local = range(1, self.total_teams+1)
    #     road = range(1, self.total_teams+1)
    #     day = range(1, self.total_days+1)
    #     slot = range(1, self.slots_per_day+1)
    #     prod = product(local, road, day, slot)
    #     vars = filter(lambda x: x[0]!=x[1], prod)
    #     vars = map(lambda x: self.format_vars(x[0], x[1], x[2], x[3]), vars)
    #     return list(vars)

