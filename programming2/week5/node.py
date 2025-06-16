''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/24
lab: lab#1005C
last modified: 3/24
purpose: node definition
'''

class Node:
    def __init__(self, entry, next_node = None):
        self.entry = entry
        self.next = next_node