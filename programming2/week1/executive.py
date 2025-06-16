''' 
author: wazeen hoq 
kuid: 3137691 
date: 2/2
lab: lab#1005c 
last modified: 2/3 
purpose: week1 exercise1 - boardgames 
'''

import csv
from boardgame import BoardGame

class Executive:
    def __init__(self, file_name): 
        #Initiatliation block
        self.file_name = file_name
        self.games = []
        self.load_games()
    
    def load_games(self):
        #Reads and loads data from gibbons-boardgames.tsv and stores in self.games
        try:
            with open(self.file_name, 'r', encoding = 'utf-8') as file:
                reader = csv.reader(file, delimiter = '\t')
                next(reader) #Skips the header row
                for row in reader:
                    if len(row) == 6:
                        try:
                            self.games.append(BoardGame(row[0], float(row[1]), float(row[2]), float(row[3]), int(row[4]), int(row[5])))
                        except ValueError:
                            print(f"Corrupt data detected and skipped: {row}")
        except FileNotFoundError:
            print("Error: File not found.")

    def run(self): 
        #Choice block
        while True:
            print("---Menu---")
            print("1. Show all games sorted by rating")
            print("2. Show games from a specific year")
            print("3. Show games by max weight")
            print("4. Compare ratings")
            print("5. Show best player count")
            print("6. Exit")

            choice = input("Choice: ")
            if choice == "1":
                self.display_sorted_games()
            elif choice == "2":
                self.display_games_by_year()
            elif choice == "3":
                self.display_games_by_weight()
            elif choice == "4":
                self.compare_ratings()
            elif choice == "5":
                self.display_games_by_players()
            elif choice == "6":
                print("Exiting program.")  
                break
            else:
                print("Error. Please enter a valid option")

#Method definition blocks     
    def display_sorted_games(self):
        sorted_games = self.games[:]
        for i in range(len(sorted_games)):
            for j in range(i+1, len(sorted_games)):
                if sorted_games[i].gibbons_rating < sorted_games[j].gibbons_rating:
                    sorted_games[i], sorted_games[j] = sorted_games[j], sorted_games[i]
                    #Above line swaps sorted_games[i] and sorted_games[j] in place without needing a temporary variable.
        for game in sorted_games:
            print(game)

    def display_games_by_year(self):
        year = input("Enter year: ")
        if year.isdigit():
            year = int(year)
            matches = [game for game in self.games if game.year_published == year]
            if matches:
                for game in matches:
                    print(game)
            else:
                print("No games found for the specified year.")
        else:
            print("Invalid input. Please enter a valid year.")

    def display_games_by_weight(self):
        try:
            max_weight = float(input("Enter max weight(0-5): "))
            for game in self.games:
                if game.avg_weight <= max_weight:
                    print(game)
        except ValueError:
            print("Error. Please enter a valid number.")
        
    def compare_ratings(self):
        try:
            threshold = float(input("Enter rating gap: "))
            for game in self.games:
                if abs(game.gibbons_rating - game.avg_rating) >= threshold:
                    print(game)
        except ValueError:
            print("Error. Please enter a valid number.")
    
    def display_games_by_players(self):
        try:
            player_count = int(input("Enter preferred lobby count: "))
            for game in self.games:
                if game.best_player_count == player_count:
                    print(game)
        except ValueError:
            print("Error. Please enter a valid number.")


