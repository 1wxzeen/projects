''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/10
lab: lab#1005C
last modified: 3/10
purpose: outbreak returns
'''

def days_flu(day):
    #base cases defined in the question
    if day == 1:
        return 6
    elif day == 2:
        return 20
    elif day == 3:
        return 75
    
    #for the recusrive case
    return days_flu(day - 1) + days_flu(day - 2) + days_flu(day - 3)

def main():
    print("OUTBREAK!")

    try:
        #the value for day (lets call n) represents the nth day for the outbreak
        day = int(input("What day do you want a sick count for: "))
        if day <= 0:
            print("Invalid number of days")
            return
    except ValueError:
        print("Invalid input; day must be an integer")
        return
    
    total = days_flu(day)
    #nth day for the outbreak
    print(f"Total people with the flu on day {day}: {total}")

    if __name__ == "__main__":
        main()
    