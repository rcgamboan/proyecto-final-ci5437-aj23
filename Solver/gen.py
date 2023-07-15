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
    def __init__(self, total_teams, 
                total_days, slots_per_day,teams=None):
        self.total_teams = total_teams
        self.total_days = total_days
        self.slots_per_day = slots_per_day
        self.vars = VarsGenerator(self.total_teams, self.total_days, self.slots_per_day)
        self.generate_bi_dict()
        self.teams = teams
        
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

    # Restricciones
    def each_team_plays_with_another_exactly_one_time(self):
        'Cada equipo debe jugar contra otro exactamente una vez'
        for local_team in range(1, self.total_teams+1):
            for road_team in range(1, self.total_teams+1):
                if local_team == road_team: continue
                vars = self.vars.generate_days_with_teams(local_team, road_team)

                self.increase_outputs(sum_greater_or_equal(self.bidict, vars, 1))                
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))
                

    def at_most_one_game_a_day_per_team(self):
        'A lo mas un equipo puede jugar una vez por dia'
        for team in range(1, self.total_teams+1):
            for day in range(1, self.total_days+1):
                vars = self.vars.generate_days_per_team(team, day)                
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

    def only_one_game_per_day_and_slot(self):
        'No puede haber dos juegos al mismo tiempo'
        for day in range(1, self.total_days+1):
            for slot in range(1, self.slots_per_day+1):
                vars = self.vars.generate_teams_per_day_and_slot(day, slot)

                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

    def no_two_consecutive_local_games_per_team(self):
        'Un equipo no puede jugar como local dos dias seguidos'        
        for team in range(1, self.total_teams+1):           
            for day in range(1, self.total_days):                
                vars = self.vars.generate_no_consecutive_local_games(team, day)
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

    def no_two_consecutive_away_games_per_team(self):
        'Un equipo no puede jugar como visitante dos dias seguidos'        
        for team in range(1, self.total_teams+1):           
            for day in range(1, self.total_days):                
                vars = self.vars.generate_no_consecutive_away_games(team, day)
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))



    ##############

    def call_glucose(self):
        subprocess.run(['./glucose', CNF_FILE_NAME, GLUCOSE_FILE_NAME,  '-model', '-verb=0'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def parse_output(self):
        if not self.output: return None
        vars = self.output.split()
        vars = list(filter(lambda x: int(x) > 0, vars))
        output = [self.bidict.inverse[var] for var in vars]
        parser = Parser(output, self.total_teams, self.total_days, self.slots_per_day, self.teams)
        self.output = parser.parse_vars()
        
        
    def solve(self):
        self.each_team_plays_with_another_exactly_one_time()
        self.at_most_one_game_a_day_per_team()
        self.only_one_game_per_day_and_slot()
        self.no_two_consecutive_local_games_per_team()
        self.no_two_consecutive_away_games_per_team()
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
            

                           

                

    
