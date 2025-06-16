''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/21
lab: lab#1005C
last modified: 4/21
purpose: main pokemon
'''

from bst import BinarySearchTree


class Pokemon:
    def __init__(self, us_name, pokedex_number, jp_name):
        self.us_name = us_name
        self.pokedex_number = int(pokedex_number)
        self.jp_name = jp_name

    def __str__(self):
        return f"{self.us_name} ({self.pokedex_number}) [{self.jp_name}]"

    def __lt__(self, other):
        return self.pokedex_number < other.pokedex_number

    def __gt__(self, other):
        return self.pokedex_number > other.pokedex_number

    def __eq__(self, other):
        return self.pokedex_number == other.pokedex_number

    def get_key(self):
        return self.pokedex_number
def load_pokemon_file(filename):
    bst = BinarySearchTree()
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                us, num, jp = parts
                try:
                    bst.insert(Pokemon(us, num, jp))
                except RuntimeError:
                    pass  # Skip duplicates silently
    return bst


def print_menu():
    print("\nOptions:")
    print("1. Add Pokemon")
    print("2. Search Pokemon")
    print("3. Print Pokedex")
    print("4. Remove Pokemon")
    print("5. Copy Tree")
    print("6. Quit")


def main():
    filename = input("Enter pokemon file (e.g., pokemon.txt): ")
    original_tree = load_pokemon_file(filename)
    copied_tree = None
    using_copy = False

    while True:
        print_menu()
        choice = input("Choose (1–6): ").strip()

        current_tree = copied_tree if using_copy else original_tree

        if choice == "1":
            us = input("American name: ")
            num = input("Pokedex #: ")
            jp = input("Japanese name: ")
            try:
                current_tree.insert(Pokemon(us, num, jp))
                print("Added.")
            except RuntimeError:
                print("Duplicate! Not added.")

        elif choice == "2":
            try:
                key = int(input("Pokedex # to search: "))
                result = current_tree.search(key)
                print(result)
            except Exception:
                print("Not found.")

        elif choice == "3":
            order = input("Traversal (in/pre/post): ").lower()
            if order == "in":
                current_tree.in_order(print)
            elif order == "pre":
                current_tree.pre_order(print)
            elif order == "post":
                current_tree.post_order(print)
            else:
                print("Invalid traversal type.")

        elif choice == "4":
            try:
                key = int(input("Pokedex # to remove: "))
                current_tree.remove(key)
                print("Removed.")
            except Exception:
                print("Not found or cannot remove.")

        elif choice == "5":
            if copied_tree:
                print("Copy already made.")
            else:
                copied_tree = original_tree.copy()
                print("Copy created.")
            use_copy = input("Use copied tree now? (y/n): ").lower()
            using_copy = (use_copy == "y")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()