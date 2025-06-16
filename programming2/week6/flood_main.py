''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/31
lab: lab#1005C
last modified: 4/06
purpose: Flood! - main.py
'''

from floodmap import FloodMap

def main():
    try:
        filename = input("map file: ")
        flood = FloodMap(filename)
        flood.run()
    except ValueError:
        print("invalid format")
    except FileNotFoundError:
        print("file not found")

if __name__ == '__main__':
    main()

#check README for notes on how I ran program