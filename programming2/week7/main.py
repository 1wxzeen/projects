from bst import BST

def main():
    bst = BST()
    while True:
        print("\nUser Menu:")
        print("1. Add")
        print("2. Print")
        print("3. Quit")

        choice = input("User input option: ").strip()

        if choice == "1":
            try:
                nums = input("Enter comma-separated numbers to add: ").split(",")
                for num in nums:
                    bst.add(int(num.strip()))
                print("Numbers added successfully.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "2":
            order = input("Traversal order (pre/in/post): ").lower()
            output = []

            def collect(value):
                output.append(str(value))

            if order == "pre":
                bst.preorder(collect)
            elif order == "in":
                bst.inorder(collect)
            elif order == "post":
                bst.postorder(collect)
            else:
                print("Invalid order. Choose pre, in, or post.")
                continue

            print("Traversal result:", " ".join(output))

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Choice not valid")



if __name__ == "__main__":
    main()