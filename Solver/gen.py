from variables.generators import (
    VarsGenerator,
    generate_partitions
)

from variables.Parser import (
    Parser
)

from variables.condicionales import (
    sum_greater_or_equal,
    sum_less_or_equal
    
)
from bidict import bidict
import subprocess
import sys

GLUCOSE_PATH = './'
CNF_FILE_NAME = 'cnf.cnf'
GLUCOSE_FILE_NAME = 'gluc.gluc'

class SatSolver():
    def __init__(self, board):
        self.board = board
        self.total_values = 9
        self.vars = VarsGenerator(board, self.total_values)
        self.generate_bi_dict()
        

        self.clauses = 0
        self.constraints = ''
        

    def generate_bi_dict(self):
        vars_set = self.vars.generate_variables()
        
        glucose_vars = range(1, len(vars_set)+1)
        vars_dict = {var:str(glucose_var) for var, glucose_var in zip(vars_set, glucose_vars)}
        self.bidict = bidict(vars_dict)
        

    def increase_outputs(self, args):        
        self.constraints += args[0]
        self.clauses += args[1]

    ##############

    def exactly_one_value_in_cell(self):
        'Una celda solo puede contener un valor'
        for row, col in self.vars.white_cells:
            
            vars = self.vars.generate_values_per_cell(row, col)
            self.increase_outputs(sum_greater_or_equal(self.bidict, vars, 1))
            self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

    def unique_values_in_sums(self):
        'No se pueden repetir valores por fila de celdas adjacentes'
        for row in self.vars.adjacent_cells_rows:
            for value in range(1, self.total_values+1):
                vars = self.vars.generate_adjacent_cells_per_value(row, value)
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

        for col in self.vars.adjacent_cells_cols:
            for value in range(1, self.total_values+1):
                vars = self.vars.generate_adjacent_cells_per_value(col, value)                
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

    def row_contains_value(self):
        'Variables que indican si una fila contiene un valor'
        row_contain_value = "fc"
        for row in self.vars.adjacent_cells_rows:
            for value in range(1, self.total_values+1):
                cont = self.bidict[self.vars.format_var(row[0][0], row[0][1], value, row_contain_value)]
                
                for cell in row:
                    constraint = f"{cont} -" + self.bidict[self.vars.format_var(cell[0], cell[1], value)]
                    constraint += " 0\n"
                    self.increase_outputs((constraint, 1))


                cont =f"-{cont}"
                for cell in row:
                    cont += " " + self.bidict[self.vars.format_var(cell[0], cell[1], value)]
                cont += " 0\n"
                self.increase_outputs((cont, 1))


    def col_contains_value(self):
        'Variables que indican si una columna contiene un valor'
        col_contain_value = "cc"
        for col in self.vars.adjacent_cells_cols:
            for value in range(1, self.total_values+1):
                cont = self.bidict[self.vars.format_var(col[0][0], col[0][1], value, col_contain_value)]
                
                for cell in col:
                    constraint = f"{cont} -" + self.bidict[self.vars.format_var(cell[0], cell[1], value)]
                    constraint += " 0\n"
                    self.increase_outputs((constraint, 1))


                cont =f"-{cont}"
                for cell in col:
                    cont += " " + self.bidict[self.vars.format_var(cell[0], cell[1], value)]
                cont += " 0\n"
                self.increase_outputs((cont, 1))

    def row_partitions_add(self):
        'Calcula las posibles particiones que pueden resolver una fila'
        row_contain_value = "fc"
        for row in self.vars.adjacent_cells_rows:            
            objective_value = self.board.get_cell(row[0][0]-1, row[0][1]-2)[1]
            partitions = generate_partitions(objective_value, len(row), 9)

            partition_variables = []
            for partition in partitions:
                var = self.bidict[self.vars.format_var(row[0][0], row[0][1]-1, 0, str(partition))]
                constraint = f"{var}"
                partition_variables.append(f"{var}")
                for value in partition:
                    constraint += f" -{self.bidict[self.vars.format_var(row[0][0], row[0][1], value, row_contain_value)]}"
                constraint += " 0\n"
                self.increase_outputs((constraint, 1))
                
                for value in partition:
                    constraint = f"-{var}"
                    constraint += f" {self.bidict[self.vars.format_var(row[0][0], row[0][1], value, row_contain_value)]} 0\n"
                    self.increase_outputs((constraint, 1))
            
            constraint = " ".join(partition_variables)
            constraint += " 0\n"
            self.increase_outputs((constraint, 1))

    def col_partitions_add(self):
        'Calcula las posibles particiones que pueden resolver una columna'
        col_contain_value = "cc"
        for col in self.vars.adjacent_cells_cols:            
            objective_value = self.board.get_cell(col[0][0]-2, col[0][1]-1)[0]
            partitions = generate_partitions(objective_value, len(col), 9)

            partition_variables = []
            for partition in partitions:
                var = self.bidict[self.vars.format_var(col[0][0], col[0][1]-1, 0, str(partition))]
                constraint = f"{var}"
                partition_variables.append(f"{var}")
                for value in partition:
                    constraint += f" -{self.bidict[self.vars.format_var(col[0][0], col[0][1], value, col_contain_value)]}"
                constraint += " 0\n"
                self.increase_outputs((constraint, 1))
                
                for value in partition:
                    constraint = f"-{var}"
                    constraint += f" {self.bidict[self.vars.format_var(col[0][0], col[0][1], value, col_contain_value)]} 0\n"
                    self.increase_outputs((constraint, 1))
            
            constraint = " ".join(partition_variables)
            constraint += " 0\n"
            self.increase_outputs((constraint, 1))
            

    def call_glucose(self):
        subprocess.run(['./glucose', CNF_FILE_NAME, GLUCOSE_FILE_NAME,  '-model', '-verb=0'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def parse_output(self):
        if not self.output: return None
        vars = self.output.split()
        vars = list(filter(lambda x: int(x) > 0, vars))
        output = [self.bidict.inverse[var] for var in vars]
        self.parser = Parser(output, self.board.row, self.board.col, self.total_values)
        output = self.parser.parse_vars()
        self.output = output       
        
       
        
    def solve(self):

        self.exactly_one_value_in_cell()
        self.unique_values_in_sums()
        self.row_contains_value()
        self.col_contains_value()
        self.row_partitions_add()
        self.col_partitions_add()
        self.constraints = f'p cnf {len(self.bidict)} {self.clauses}\n{self.constraints}'

        with open(CNF_FILE_NAME, 'w') as f:
            f.write(self.constraints)
            f.close()

        self.call_glucose()

        with open(GLUCOSE_FILE_NAME, 'r') as f:
            self.output = f.readline().strip()
            if self.output == "UNSAT":
                self.output = None
        self.parse_output()
        
        return self.output
            

                           

                

    
