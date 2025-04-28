import sys


def repl():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        
        print(f"{command}: command not found")


def main():
    # Uncomment this block to pass the first stage
    repl()
    


if __name__ == "__main__":
    main()
