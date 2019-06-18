# Project_2_Soccer_Data
Flatiron School Project for Module 2 by David Hasse and Tino Pietrassyk

## Getting Started
Run: Start_Here.ipynb

## Description

Running the notebook file will return as list of summary statistics for each team for
the chosen Year and Divisions of Soccermatches.
The Requested Data will be written into a MongoDB.

### Input
This Project is based on the Soccer Games Data-Set found here:

[kaggle page](https://www.kaggle.com/laudanum/footballdelphi)

Database contains Records of Soccer games in the German Bundesliga 1 and 2 as well as 
The UK Premier league.

To select A Season as well as a Subset of Divisions -- pass the year as
an INT and the Divisions abbreviations as as List of STR when calling
the Season Object.
Possible Arguments for League: <br>
+ "D1" = 1. Bundesliga
+ "D2" = 2. Bundesliga
+ "E0" = Premier League

### Computation

1. Getting Data From The DB
2. Write data to Season class at instantiation
3. Instantiate Teams
    1. get stadium location via Google API
4. Instantiate Games
    1. get weather data via DarkSky API
5. Compute summary statistics
    1. print bar-plots as .png-Files to /Figures/<'Season>/
6. Write Information to MongoDB called euro_football
