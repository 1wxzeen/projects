''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/27
lab: lab#1005C
last modified: 4/28
purpose: main file
'''
from hospital import Hospital

def main():
    hospital = Hospital()
    try:
        with open("input", "r") as file:  # input file is named 'input'
            for line in file:
                line = line.strip()
                if line.startswith("ARRIVE"):
                    parts = line.split()
                    first_name = parts[1]
                    last_name = parts[2]
                    age = parts[3]
                    illness = parts[4]
                    severity = parts[5]
                    hospital.arrive(first_name, last_name, age, illness, severity)
                elif line == "NEXT":
                    hospital.next_patient()
                elif line == "TREAT":
                    hospital.treat()
                elif line == "COUNT":
                    hospital.count()
    except FileNotFoundError:
        print("Input file not found.")

if __name__ == "__main__":
    main()

#use README for instructions as to how I ran the file, as I didnt use import sys
#input file is read directly