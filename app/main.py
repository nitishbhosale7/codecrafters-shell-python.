import sys
import os
import shlex
import subprocess
import readline

class Shell:
    def __init__(self):
        self.history = []
        self.builtins = ["echo", "exit", "cd", "pwd", "type"]
        self.complete_state = 0
        self.setup_autocomplete()

    def setup_autocomplete(self):
        """Set up tab completion."""
        readline.set_completer(self.tab_completer)
        readline.parse_and_bind("tab: complete")

    def start(self):
        self.repl()

    def repl(self):
        while True:
            sys.stdout.write("$ ")  # Print the prompt
            command = input()
            self.history.append(command)

            try:
                parts = shlex.split(command)
            except ValueError as e:
                print(f"Error parsing command: {e}")
                continue
            
            if not parts:
                continue
            
            initial_command = parts[0]
            args = parts[1:]

            if self.execute(initial_command, args) == 0:
                break

    def get_path_by_command_name(self, command_name):
        path_variables = os.environ.get('PATH').split(os.pathsep)
        for path in path_variables:
            extracted_path = os.path.join(path, command_name)
            if os.path.exists(extracted_path):
                return extracted_path
        return None

    def execute(self, command, args):
        if command == "exit":
            return 0
        elif command == "echo":
            print(" ".join(args))
        elif command == "type":
            next_command = args[0] if args else None
            if next_command in self.builtins:
                print(f"{next_command} is a shell builtin")
            else:
                command_path = self.get_path_by_command_name(next_command)
                if command_path:
                    print(f"{next_command} is {command_path}")
                else:
                    print(f"{next_command} not found")
        elif command == "pwd":
            print(os.getcwd())
        elif command == "cd":
            if args:
                try:
                    os.chdir(os.path.expanduser(args[0]))
                except FileNotFoundError:
                    print(f"{args[0]}: No such file or directory")
            else:
                print("cd: missing argument.")
        else:
            command_path = self.get_path_by_command_name(command)
            if command_path:
                subprocess.run([command] + args)
            else:
                print(f"{command}: command not found")
        return None
    
    def tab_completer(self, text, state):
        """Completer function for tab completion."""
        matches = [m for m in self.builtins if m.startswith(text)]
        
        # Add external executables to the matches
        path_variables = os.environ.get('PATH').split(os.pathsep)
        for path in path_variables:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.startswith(text) and os.access(os.path.join(path, file), os.X_OK):
                        matches.append(file)

        if state == 0:  # First call for this input, generate options
            self.complete_state = 1  # Indicate first TAB press
            if len(matches) > 1:
                sys.stdout.write("\a")  # Ring the bell
            return matches[state] + " " if state < len(matches) else None
        elif state < len(matches):
            return matches[state] + " "
        else:
            if self.complete_state == 1 and len(matches) > 1:
                print("\n" + "  ".join(matches))
                self.complete_state = 0  # Reset state after displaying matches
            return None  # No more matches

def main():
    terminal = Shell()
    try:
        terminal.start()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()