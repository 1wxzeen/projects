''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/24
lab: lab#1005C
last modified: 3/30
purpose: LinkedList definition
'''

from node import Node

class LinkedList:
    def __init__(self):
        self._front = None
        self._length = 0

    def length(self):
        return self._length
    
    def clear(self):
        self._front = None
        self._length = 0

    def insert(self, index, entry):
        if index < 0 or index > self._length: #only one we use just > on the self._length
            #this is since we can go one over the last index
            raise IndexError("invalid index")

        new_node = Node(entry)

        if index == 0:
            new_node.next = self._front #you are making the front of the node to the next element after new_node
            self._front = new_node #youre making the new node the front of the list
        
        else:
            previous = self._get_node(index - 1)
            new_node.next = previous.next
            previous.next = new_node

        self._length += 1

    def remove(self, index): #cant go one over the last index so it has to be >=
        if index < 0 or index >= self._length:
            raise IndexError
        
        if index == 0:
            target = self._front
            self._front = target.next
        
        else:
            previous = self._get_node(index - 1)
            target = previous.next 
            previous.next = target.next 
        
        self._length -= 1
        return target.entry
    
    def get_entry(self, index):
        if index < 0 or index >= self._length: #greater than or equal to since the last index is length - 1
            raise IndexError
        
        jumper = self._front
        for i in range(index):
            jumper = jumper.next
        
        return jumper.entry #only here do we depackage the node and get the entry
    
    def set_entry(self, index, entry):
        #its like a replace funciton where oyu replace a node with another node at the specified index
        if index < 0 or index >= self._length:
            raise IndexError("invalid index")
        node = self._get_node(index)
        node.entry = entry

    def _get_node(self, index):
        #Private helper to return the node at a given index.
        if index < 0 or index >= self._length:
            raise IndexError("invalid index")
        current = self._front
        for i in range(index):
            current = current.next
        return current
    
    def __iter__(self):
        #Iterator to allow looping over the list entries.
        current = self._front
        while current:
            yield current.entry
            current = current.next
