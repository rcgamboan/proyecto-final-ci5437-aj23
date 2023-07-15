from itertools import product
class VarsGenerator():
    def __init__(self, total_teams, total_days, slots_per_day):
        self.total_teams = total_teams
        self.total_days = total_days
        self.slots_per_day = slots_per_day
        self.len_total_teams = len(str(total_teams))
        self.len_total_days = len(str(total_days))
        self.len_slots_per_day = len(str(slots_per_day))

    def format(self, var, len):
        x =  "{:0" + str(len) + "}"
        return x.format(var)

    def format_team(self, team):
        return self.format(team, self.len_total_teams)

    def format_day(self, day):
        return self.format(day, self.len_total_days)

    def format_slot(self, slot):
        return self.format(slot, self.len_slots_per_day)

    def format_vars(self, local_team, road_team, day, slot):
        assert len(str(local_team)) <= self.len_total_teams
        assert len(str(road_team)) <= self.len_total_teams
        assert len(str(day)) <= self.len_total_days
        assert len(str(slot)) <= self.len_slots_per_day
        return ''.join([
            self.format_team(local_team),
            self.format_team(road_team),
            self.format_day(day),
            self.format_slot(slot)
        ])

    def generate_variables(self):
        vars = []
        local = range(1, self.total_teams+1)
        road = range(1, self.total_teams+1)
        day = range(1, self.total_days+1)
        slot = range(1, self.slots_per_day+1)
        prod = product(local, road, day, slot)
        vars = filter(lambda x: x[0]!=x[1], prod)
        vars = map(lambda x: self.format_vars(x[0], x[1], x[2], x[3]), vars)
        return list(vars)

    def generate_days_with_teams(self, local_team, road_team):
        vars = []
        for day in range(1, self.total_days+1):
            for slot in range(1, self.slots_per_day+1):
                vars.append(self.format_vars(local_team, road_team, day, slot))

        return vars

    def generate_days_per_team(self, team, day):
        vars = []
        for oponent in range(1, self.total_teams+1):
            if oponent == team: continue
            for slot in range(1, self.slots_per_day+1):
                vars.append(self.format_vars(team, oponent, day, slot))
                vars.append(self.format_vars(oponent, team, day, slot))

        return vars

    def generate_teams_per_day_and_slot(self, day, slot):
        vars = []
        for local in range(1, self.total_teams+1):
            for away in range(1, self.total_teams+1):
                if local == away: continue  
                vars.append(self.format_vars(local, away, day, slot))
        return vars

    def generate_no_consecutive_local_games(self, team, day):
        vars = []
        for oponent in range(1, self.total_teams+1):
            if team == oponent: continue        
            for slot in range(1, self.slots_per_day+1):            
                vars.append(self.format_vars(team, oponent, day, slot))
                vars.append(self.format_vars(team, oponent, day+1, slot))
        return vars

    def generate_no_consecutive_away_games(self, team, day):
        vars = []
        for oponent in range(1, self.total_teams+1):
            if team == oponent: continue        
            for slot in range(1, self.slots_per_day+1):            
                vars.append(self.format_vars(oponent, team, day, slot))
                vars.append(self.format_vars(oponent, team, day+1, slot))
        return vars
