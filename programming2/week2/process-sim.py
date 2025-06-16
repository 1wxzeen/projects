''' 
author: wazeen hoq 
kuid: 3137691 
date: 2/10 
lab: lab#3 
last modified: 2/10 
purpose: process simulator
'''

class Node:
    def __init__(self, entry):
        self.entry = entry
        self.next = next

class LinkedStack:
    #Stack class implemented as linkedlist
    def __init__(self):
        self.top = None

    def push(self, entry):
        new_node = Node(entry) #makes node
        new_node.next = self.top #puts it on top of stack
        self.top = new_node #updates top

    def pop(self):
        if self.is_empty():
            raise RuntimeError("Empty stack")
        popped = self.top.entry #grabs top of stack
        self.top = self.top.next #moves to nexxt in stack
        return popped #returns the grabbed item from stack 
    
    def peek(self):
        if self.is_empty():
            raise RuntimeError("Empty stac")
        return self.top.entry
    
    def is_empty(self):
        return self.top is None
    
class Function:
    def __init__(self, name, can_handle_exception):
        self.name = name
        self.can_handle_exception = (can_handle_exception.lower() == "yes")

class Process:
    def __init__(self, name):
        self.name = name
        self.call_stack = LinkedStack() #stack of function calls
        print(f"{self.name} Process started")
        self.call_stack.push(Function("main", True)) #to  start with main

    def call_function(self, function_name, can_handle_exception):
        print(f"{self.name} calls {function_name} function")
        self.call_stack.push(Function(function_name, can_handle_exception)) #add to stack

    def return_function(self):
        if self.call_stack.is_empty():
            print("Error: no function to return from")
            return
        func = self.call_stack.pop() #removes last function from stack
        print(f"{self.name} has {func.name} return")
        if self.call_stack.is_empty():
            print(f"{self.name} has main return. {self.name} Process ended")

    def raise_exception(self):
        print(f"{self.name} has {self.call_stack.peek().name} raise an exception")
        while not self.call_stack.is_empty(): #Keep popping off functions until finds one that can handle it
            func = self.call_stack.pop()
            if func.can_handle_exception:
                print(f"{self.name} has {func.name} works and runs")
                return
            else:
                print(f"{self.name} pop {func.name} off call stack")
        print(f"{self.name} has main return. {self.name} Process ended")

# Driver function
if __name__ == "__main__":
    file_name = input("Enter the input file name: ")
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: Input file not found.")
        exit()
    
    process = None #no process yet
    for line in lines:
        parts = line.strip().split() #splits into words
        if not parts:
            continue #skips the empty lines, if any
        command = parts[0].upper()
        if command == "START":
            if process is not None:
                print("Error: Process already started.")
            else:
                process = Process(parts[1])
        elif command == "CALL":
            if process is None:
                print("Error: No active process.")
            else:
                process.call_function(parts[1], parts[2])
        elif command == "RETURN":
            if process is None:
                print("Error: No active process.")
            else:
                process.return_function()
        elif command == "RAISE":
            if process is None:
                print("Error: No active process.")
            else:
                process.raise_exception()
        else:
            print(f"Error: Invalid command {command}")


                             