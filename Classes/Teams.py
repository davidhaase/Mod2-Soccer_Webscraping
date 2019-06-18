import matplotlib.pyplot as plt

####################
#######CLASS########
####################

class Team():
    """Class Contains Team Statistics derived from listening on the Creation of Game instences"""
    def __init__(self,ID,name):
        #Basic information and empty containers
        self.id = ID
        self.name = name
        self.goal_counter = 0
        self.win_counter = 0
        self.loss_counter = 0
        self.tie_counter = 0
        self.winning_percentage = 0
        self.rain_winning_percentage = 0
        self.stadium_location = "implement location getter"
        self.num_of_games_played = 0
        self.num_of_rain_games = 0
        #self.figure = 0
        self.figure_path = ""
        self.team_games_list = []

    def get_win_percentage(self):
        """Calculate and update overall winning percentage - returns FLOAT"""
        self.winning_percentage = self.win_counter/self.num_of_games_played
        return self.winning_percentage

    def get_rain_win_percentage(self):
        """ Calculate and update winning percentage for games in the rain,
        returns:    LIST of GAMES Objects where Rain ,
                    LIST of GAMES Objects where Rain and Win"""
        rain_games = list(filter (lambda game: game.is_rain, self.team_games_list))
        rain_wins = list(filter(lambda game: game.winner == self, rain_games))
        self.rain_winning_percentage = len(rain_wins)/len(rain_games)
        self.num_of_rain_games = len(rain_games)
        return rain_games ,rain_wins , self.rain_winning_percentage

    def plot(self, save = False, dir =""):
        """ Shows Plot of the Absolute Wins, Losses and Ties
            parameters: save BOOL (Will Save Plot as .png)
                        dir STR (specify subdirectory for image storing"""

        plt.style.use('ggplot')
        fig = plt.figure(figsize=(5, 6));
        x = [1, 2, 3]
        y = [self.win_counter, self.loss_counter, self.tie_counter]
        plt.bar(x, y, tick_label=["Win", "Loss", "Tie"], color=("g", "r", "y"))
        plt.ylim((0, 34))
        plt.title(f"{self.name} - game results")
        plt.ylabel("Number of Games (#)")

        #Saving to File and attach path to Team Object
        if save:
            plt.savefig(dir+self.name+".png");
            self.figure_path = dir+self.name[0:]
            #self.figure = fig
            plt.close(fig)

    def to_dict(self):
        """Will return all Attributes as a dict suitable for MongoDB sotring"""
        out_dict = self.__dict__

        #work around bug that mongo DB wont accept objects
        out_dict["team_games_list"] = []#[f"{game.date} @{game.home_team}" for game in self.team_games_list]
        return out_dict