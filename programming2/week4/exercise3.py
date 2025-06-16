''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/10
lab: lab#1005C
last modified: 3/10
purpose: fibonacci
'''

def fibonacci(n):
    #returns the nth element in the sequence
    #base cases
    if n == 0:
        return 0 
    elif n == 1:
        return 1
    
    #recusive case
    return fibonacci(n - 1) + fibonacci(n - 2)

def is_fibonacci(num, a = 0, b = 1):
    #returns if the input num is a fibonacci number or not
    #base case
    if num == a or num == b:
        return True
    elif b > num:
        return False
    
    #resuive
    return is_fibonacci(num, b, a + b)

def main():
    try:
        user_input = input("Enter a mode and value: ").strip().split()
        #to check for length of user string being 2
        if len(user_input) != 2:
            print("Invalid input. Use '-i Number_input' or '-v Number_input'.")
            return #stops mmain to allow for user to re-run
        
        #Dividing the user input into 2 possible things (index, value) means we can check either the ith number in the sequnece or if the number v is in the sequnece
        #i represents the index of elements in the sequence
        #v represents the values in the sequence

    
        mode, value = user_input
        value = int(value)

        #indexing into the sequence to obtain the ith element
        if mode == "-i":
            if value < 0:
                print("Index must be greater than or equal to 0")
                return
            fibonacci_value = fibonacci(value)
            print(fibonacci_value)

        #checkign if the value v is in the sequence
        elif mode == "-v":
            if value < 0:
                print("Negative numbers arent in the sequence")
                return
            if is_fibonacci(value):
                print(f"{value} is in the sequence")

            else:
                print(f"{value} is not in the sequence")

        #if the mode isnt -i or -v   
        else:
            printggg("Invalid mode")

    #now checking in the number after the mode is an integer or not
    #need this becuase of value = int(value)
    except ValueError:
        print("Invalid input; must be an integer")

if __name__ == "__main__":
    main()

        
