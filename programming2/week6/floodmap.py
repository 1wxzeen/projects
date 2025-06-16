''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/06
lab: lab#1005C
last modified: 4/06
purpose: floodmap class
'''

class FloodMap:
    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = [line.rstrip('\n') for line in file]
        except FileNotFoundError:
            raise SystemExit("file not found")

        try:
            self.start_row, self.start_col = map(int, lines[0].split())
            self.water = int(lines[1])
        except:
            print("invalid format")
            return
        
        self.map = [list(row) for row in lines[2:]]
        self.numRows = len(self.map)
        self.numCols = len(self.map[0]) if self.numRows > 0 else 0


        if self.numRows < 1 or self.numCols < 1:
            print("Invalid map size")
            return

        if not (0 <= self.start_row < self.numRows and 0 <= self.start_col < self.numCols):
            print("Invalid starting position")
            return

        if self.map[self.start_row][self.start_col] != ' ':
            print("Invalid starting position")
            return

    def flood_fill(self, row, col):
        if self.water <= 0:
            return

        if not (0 <= row < self.numRows and 0 <= col < self.numCols):
            return

        if self.map[row][col] != ' ':
            return
        
        self.map[row][col] = '~'
        self.water -= 1

        self.flood_fill(row - 1, col)  # up
        self.flood_fill(row, col + 1)  # right
        self.flood_fill(row + 1, col)  # down
        self.flood_fill(row, col - 1)  # left

    def run(self):
        print(f"Size: {self.numCols},{self.numRows}")
        print(f"Starting position: {self.start_row},{self.start_col}")

        self.flood_fill(self.start_row, self.start_col)

        for row in self.map:
            print("".join(row))

        if self.water == 0:
            print("Flood ran out of water.")
        else:
            print("Flood complete.")
