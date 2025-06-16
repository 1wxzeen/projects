''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/27
lab: lab#1005C
last modified: 4/28
purpose: patient class
'''
class Patient:
    def __init__(self, first_name, last_name, age, illness, severity, arrival_order):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.illness = illness
        self.severity = severity
        self.arrival_order = arrival_order

#Define how to compare two patients for max-heap:

    def __lt__(self, other):
        if self.severity != other.severity:
            return self.severity < other.severity
        if self.age != other.age:
            return self.age < other.age
        return self.arrival_order > other.arrival_order

    def __str__(self):
        return (f"Name: {self.last_name}, {self.first_name}\n"
                f"Age: {self.age}\n"
                f"Suffers from: {self.illness}\n"
                f"Illness severity: {self.severity}\n"
                f"Arrival order: {self.arrival_order}")