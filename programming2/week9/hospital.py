''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/27
lab: lab#1005C
last modified: 4/28
purpose: hospital class
'''

from maxheap import MaxHeap
from patient import Patient

class Hospital:
    def __init__(self):
        self.heap = MaxHeap()
        self.arrival_counter = 1

    def arrive(self, first_name, last_name, age, illness, severity):
        patient = Patient(first_name, last_name, int(age), illness, int(severity), self.arrival_counter)
        self.arrival_counter += 1
        self.heap.push(patient)

    def next_patient(self):
        if self.heap.is_empty():
            print("There are no patients waiting.")
            return
        print("Next patient:")
        print(self.heap.peek())
        print()

    def treat(self):
        if self.heap.is_empty():
            print("There are no patients to treat.")
            return
        self.heap.pop()

    def count(self):
        num_patients = self.heap.size()
        if num_patients == 1:
            print("There is 1 patient waiting.\n")
        else:
            print(f"There are {num_patients} patients waiting.\n")
