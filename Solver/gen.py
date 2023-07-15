from variables.generators import (
    VarsGenerator
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
        self.vars = VarsGenerator(board)
        self.generate_bi_dict()
        
        
        self.clauses = 0
        self.constraints = ''

    def generate_bi_dict(self):
        vars_set =self.vars.generate_variables()
        
        glucose_vars = range(1, len(vars_set)+1)
        vars_dict = {var:str(glucose_var) for var, glucose_var in zip(vars_set, glucose_vars)}
        self.bidict = bidict(vars_dict)

    def increase_outputs(self, args):        
        self.constraints += args[0]
        self.clauses += args[1]

    ##############

    def exactly_one_value_in_cell(self):
        for row, col in self.vars.white_cells:
            
            vars = self.vars.generate_values_per_cell(row, col)
            self.increase_outputs(sum_greater_or_equal(self.bidict, vars, 1))
            self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))




    def call_glucose(self):
        subprocess.run(['./glucose', CNF_FILE_NAME, GLUCOSE_FILE_NAME,  '-model', '-verb=0'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def parse_output(self):
        if not self.output: return None
        vars = self.output.split()
        vars = list(filter(lambda x: int(x) > 0, vars))
        output = [self.bidict.inverse[var] for var in vars]
        print(output)
       
        
    def solve(self):

        self.exactly_one_value_in_cell()
        self.constraints = f'p cnf {len(self.bidict)} {self.clauses}\n{self.constraints}'

        with open(CNF_FILE_NAME, 'w') as f:
            f.write(self.constraints)
            f.close()

        print("Solving!")

        self.call_glucose()
        print("Parsing solution!")
        with open(GLUCOSE_FILE_NAME, 'r') as f:
            self.output = f.readline().strip()
            if self.output == "UNSAT":
                self.output = None
        self.parse_output()
        return self.output
            

                           

                

    
