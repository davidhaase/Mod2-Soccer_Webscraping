#Libraries
import tpclean.tpclean as tp
import os

#Locals Files
from Classes import Games, Teams

####################
#######CLASS########
####################



class Season():
    """Contains Summary information for a Season. Will instantiate Teams and Games. Will compute statisics
    Container for Teams and Games Objects"""
    teams_list = []
    games_list = []
    locations_list = []

    def __init__(self,year,divisions = [], database = "database.sqlite"):
        self.year = year
        self.figure_directory = f"./Figures/{self.year}/"

        #establish connection to database and run querry
        tp.sql_connect(database)
        divs = "','".join(divisions)
        df = tp.sql(f""" SELECT * FROM FlatView_Advanced {f" WHERE Div IN('{str(divs)}')" if divisions else ''} 
                    AND Season == {year}""")
        self.data = df

        #populate Season
        self.fill_teams()
        self.fill_games()
        self.get_statistics()
        self.print_plots()


    def get_team(self,team_to_check):
        """Inputs a Teamname as a STR and returns the according team object"""
        for team in self.teams_list:
            if(team.name == team_to_check):
                return team
        return "Team not found"

    def fill_teams(self):
        """Instantiates Team Objects for every Team in self.data"""
        df = self.data
        self.teams_list = [Teams.Team(i, df.HomeTeam.unique()[i]) for i in range(len(df.HomeTeam.unique()))]

    def fill_games(self):
        """Instantiates Game Objects for every Game in self.data"""
        self.games_list = []
        df = self.data[["Match_ID", "HomeTeam", "AwayTeam", "Season", "Date", "FTHG", "FTAG"]]
        for i in range(len(df)):
            ID = df.Match_ID[i]
            home_team = self.get_team(df.HomeTeam[i])
            away_team = self.get_team(df.AwayTeam[i])
            season = df.Season[i]
            date_list = df.Date[i].split("-")
            date = "/".join([date_list[1], date_list[2], date_list[0]])
            score_home = df.FTHG[i]
            score_away = df.FTAG[i]

            #check for Duplicates and skip them
            ID_list = [game.ID for game in self.games_list]
            if ID in ID_list:
                continue
            else:
                self.games_list.append(Games.Game(ID, home_team, away_team, season, date, score_home, score_away))

    def get_statistics(self):
        """Computes win_percentage and rain_win_percentage for every Team"""
        for team in self.teams_list:
            team.get_win_percentage()
            team.get_rain_win_percentage()

    def create_image_directory(self):
        """Creates Folder to store plots in"""
        # define the name of the directory to be created
        dirname = os.path.dirname(__file__)
        filename = "."+self.figure_directory
        try:
            os.mkdir(filename)
        except OSError:
            print("Creation of the directory %s failed" % filename)
        else:
            print("Successfully created the directory %s " % filename)

    def print_plots(self):
        """Saves plots to Folder """
        for team in self.teams_list:
            team.plot(save= True, dir= self.figure_directory)




