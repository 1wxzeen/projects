''' 
author: wazeen hoq 
kuid: 3137691 
date: 2/2
lab: lab#1005c 
last modified: 2/3 
purpose: week1 exercise1 - boardgames 
'''

from executive import Executive

def main():
    file_name = input("Enter the input file name: ")
    controller = Executive(file_name) #Create an instance of the class
    controller.run()
    print("Program finished.")

if __name__ == "__main__":
    main()
