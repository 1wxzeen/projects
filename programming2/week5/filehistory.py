''' 
author: wazeen hoq 
kuid: 3137691 
date created: 3/24
lab: lab#1005C
last modified: 3/30
purpose: file histroy
'''

from linkedlist import LinkedList

def display_menu():
    print("\nFile History Menu:")
    print("1. Add a file to history")
    print("2. Remove the most recent file from history")
    print("3. View file history")
    print("4. Clear file history")
    print("5. Exit")


def main():
    history = LinkedList()

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            filename = input("Enter the filename to add: ").strip()
            #Insert at index=0 so that the most recent file is at the front
            history.insert(0, filename)
            print(f"'{filename}' added to history.")

        elif choice == '2':
            if history.length() == 0:
                print("File history is empty. Nothing to remove.")
            else:
                removed = history.remove(0)
                print(f"Removed '{removed}' from history.")

        elif choice == '3':
            if history.length() == 0:
                print("File history is empty.")
            else:
                print("\nCurrent File History:")
                for i, file in enumerate(history):
                    print(f"{i+1}. {file}")

        elif choice == '4':
            history.clear()
            print("File history cleared.")
        
        elif choice == '5':
            print("Exiting File History Manager.")
            break
        
        else:
            #edge case
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()