''' 
author: wazeen hoq 
kuid: 3137691 
date: 2/3 
lab: lab#1005c 
last modified: 2/3 
purpose: week1 exercise1 - boardgames 
'''

class BoardGame:
    def __init__(self, name, gibbons_rating, avg_rating, avg_weight, year_published, best_player_count):
        self.name = name
        self.gibbons_rating = gibbons_rating
        self.avg_rating = avg_rating
        self.avg_weight = avg_weight
        self.year_published = year_published
        self.best_player_count = best_player_count

    def __str__(self):
        return f"""
==========
Game: {self.name}
Gibbons' Rating: {self.gibbons_rating}
Public Rating: {self.avg_rating}
Weight: {self.avg_weight}
Year: {self.year_published}
Best Players: {self.best_player_count}
==========""" #Returns stats divided by ==========
