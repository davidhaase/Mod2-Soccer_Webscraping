import numpy as np

####################
#######CLASS########
####################

class Game():
    """Contains basic game information for a soccer game"""
    def __init__(self,ID,home_team,away_team,season,date,score_home,score_away):
        #Basic Information passed from Dataframe
        self.ID = ID
        self.home_team = home_team #Team Object
        self.away_team = away_team #Team Object
        self.season = season
        self.date = date
        self.location = home_team.stadium_location
        self.score_home = int(score_home)
        self.score_away = int(score_away)
        self.winner = self.winner()
        self.looser = self.looser()
        self.is_rain = self.get_rain()

        #Set scoring records
        self.home_team.goal_counter += int(self.score_home)
        self.home_team.num_of_games_played += 1
        self.away_team.goal_counter += int(self.score_away)
        self.away_team.num_of_games_played += 1

        #Compute game result
        if self.winner:
            self.winner.win_counter +=1
        if self.looser:
            self.looser.loss_counter +=1
        if self.tie():
            for team in self.tie():
                team.tie_counter +=1

        #Store append game to the teams it was played by
        self.home_team.team_games_list.append(self)
        self.away_team.team_games_list.append(self)


    def winner(self):
        """ Determines and returns winning team object"""
        if self.score_away > self.score_home:
            return self.away_team
        if self.score_away < self.score_home:
            return self.home_team
        else:
            return None

    def looser(self):
        """ Determines and returns loosing team object"""
        if self.score_away < self.score_home:
            return self.away_team
        if self.score_away > self.score_home:
            return self.home_team
        else:
            return None

    def tie(self):
        """ Determines if game result was a draw. Returns list with both teams objects"""
        if self.score_away == self.score_home:
            return [self.home_team, self.away_team]
        else:
            return None

    def get_rain(self):
        """ Calls DarkSky API and return whether the game was rainy or not"""
        rain = np.random.choice([True,False],1)
        return rain
        #return wg.WeatherGetter().is_rain(self.date , self.home_team.name + " stadium", False)