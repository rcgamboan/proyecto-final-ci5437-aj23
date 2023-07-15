class Parser():
    def __init__(self, vars, total_teams, total_days, slots_per_day,teams=None):
        self.vars = vars
        self.total_teams = total_teams
        self.total_days = total_days
        self.slots_per_day = slots_per_day
        self.len_total_teams = len(str(total_teams))
        self.len_total_days = len(str(total_days))
        self.len_slots_per_day = len(str(slots_per_day))
        self.teams = teams

    def parse_vars(self):
        output = []
        for var in self.vars:
            local = var[:self.len_total_teams]
            away = var[self.len_total_teams:2*self.len_total_teams]
            day = var[2*self.len_total_teams:2*self.len_total_teams+self.len_total_days]
            slot = var[-self.len_slots_per_day:]
            output.append(
                Asignation(local, away, day, slot,self.teams)
            )
        return output

class Asignation():
    def __init__(self, local, away, day, slot, teams=None):
        self.local = int(local)
        self.away = int(away)
        self.day = int(day)
        self.slot = int(slot)
        self.teams = teams
        
    def __repr__(self) -> str:
        #print("\nequipos:")
        #print(self.teams)
        if self.teams == None:
            return f'{self.local} vs {self.away} {self.day}-{self.slot}'
        else:
            return f'{self.teams[self.local-1]} vs {self.teams[self.away-1]} {self.day}-{self.slot}'
        