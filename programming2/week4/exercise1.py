''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/10
lab: lab#1005C
last modified: 3/10
purpose: recursive power function
'''

def power_recursion(base, exponent):
    if exponent == 0:
        return 1 #for the base case
    
    return base * power_recursion(base, exponent-1)

def main():
    #edge case handling
    try:
        base = int(input("Enter the base: "))
    except ValueError:
        print("Please enter an integer")
        return
    
    while True: #while loop to get exponent after all missinputs
        try:
            exponent = int(input("Enter the power: "))
            if exponent < 0:
                print("Exponent must be greater than or equal to 0")
            else:
                break
        except ValueError:
            print("Input must be an integer")

    result = power_recursion(base, exponent)
    print(f"The inputs result in {result}")

if __name__ == "__main__":
    main()

