''' 
author: wazeen hoq 
kuid: 3137691 
date created: 2/16
lab: lab#1005C
last modified: 2/17 
purpose: cpu scheduling sim
'''

class Node:
    def __init__(self, entry):
        self.entry = entry
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, entry):
        new_node = Node(entry)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            raise RuntimeError("Empty stack")
        entry = self.top.entry
        self.top = self.top.next
        return entry

    def peek(self):
        if self.top is None:
            raise RuntimeError("Empty stack")
        return self.top.entry

    def is_empty(self):
        return self.top is None

class Queue:
    def __init__(self):
        self.front = self.rear = None

    def enqueue(self, entry):
        new_node = Node(entry)
        if self.rear:
            self.rear.next = new_node
        else:
            self.front = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            raise RuntimeError("Empty queue")
        entry = self.front.entry
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return entry

    def peek_front(self):
        if self.front is None:
            raise RuntimeError("Empty queue")
        return self.front.entry

    def is_empty(self):
        return self.front is None

class Function:
    def __init__(self, name, handles_exception):
        self.name = name
        self.handles_exception = handles_exception

class Process:
    def __init__(self, name):
        self.name = name
        self.call_stack = Stack()
        self.call_stack.push(Function("main", True))

    def call_function(self, function_name, handles_exception):
        self.call_stack.push(Function(function_name, handles_exception))
        print(f"{self.name} calls {function_name}")

    def return_function(self):
        if self.call_stack.top is None:
            print(f"{self.name} process ended")
            return None
        self.call_stack.pop()
        if self.call_stack.top is None:
            print(f"{self.name} process ended")
            return None
        return self

    def raise_exception(self):
        print(f"{self.name} raises an exception")
        while self.call_stack.top is not None:
            last_checked_function = self.call_stack.pop()
            print(f"Function {last_checked_function.name} popped due to exception")
            if last_checked_function.handles_exception:
                print(f"{self.name} handled exception and continued")
                return self
        print(f"{self.name} process ended due to unhandled exception")
        return None

class CPU_Scheduler:
    def __init__(self):
        self.process_queue = Queue()

    def start_process(self, name):
        process = Process(name)
        self.process_queue.enqueue(process)
        print(f"{name} added to queue")

    def execute_next(self, command, *args):
        if self.process_queue.is_empty():
            print("No processes in queue")
            return
        process = self.process_queue.dequeue()
        if command == "CALL":
            process.call_function(args[0], args[1] == "yes")
        elif command == "RETURN":
            process = process.return_function()
        elif command == "RAISE":
            process = process.raise_exception()
        if process:
            self.process_queue.enqueue(process)

    def run(self, commands):
        for cmd in commands:
            parts = cmd.split()
            if parts[0] == "START":
                self.start_process(parts[1])
            elif parts[0] in {"CALL", "RETURN", "RAISE"}:
                self.execute_next(*parts)

if __name__ == "__main__":
    scheduler = CPU_Scheduler()
    input_commands = [
        "START itunes", "START firefox", "START putty",
        "CALL play no", "CALL navigate no", "RETURN"
    ]
    scheduler.run(input_commands)