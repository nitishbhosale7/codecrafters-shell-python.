import sys
import os
import shlex

class shell:
    def __init__(self):
        self.history = []
        
    def start(self):
        self.repl()
        
    def repl(self):
        while True:
                    sys.stdout.write("$ ")  # Print the prompt

                    # Wait for user input
                    command = input()
                    self.history.append(command)
                    
                    # Use shlex.split to handle quoted strings properly
                    try:
                        parts = shlex.split(command)
                    except ValueError as e:
                        print(f"Error parsing command: {e}")
                        continue
                    
                    if not parts:
                        continue
                    
                    initial_command = parts[0]
                    args = parts[1:]

                    # Execute the command
                    if self.execute(initial_command, args) == 0:
                        break
            
    def getPathByCommandName(self, command_name):
        path_separator = os.pathsep
        path_variables = os.environ.get('PATH').split(path_separator)
        for path in path_variables:
            extracted_path = os.path.join(path, command_name)
            if os.path.exists(extracted_path):
                return extracted_path
        return None  # Return None if no path is found

    def execute(self, command, args):
        match command:
            case "exit":
                if len(args) > 0 and args[0] == "0":
                    return 0
            case "echo":
                os.system("echo " + " ".join(args))
            case "type":
                next_command = args[0]
                output_path = self.getPathByCommandName(next_command)

                match next_command:
                    case "echo":
                        print("echo is a shell builtin")
                    case "exit":
                        print("exit is a shell builtin")
                    case "pwd":
                        print("pwd is a shell builtin")
                    case "type":
                        print("type is a shell builtin")
                    case _:
                        if output_path:
                            print(f"{next_command} is {output_path}")
                        else:
                            print(f"{next_command} not found")
                            
            case "pwd":
                print(os.getcwd())
                
                
            case "cd":
                if len(args) > 0:
                    try:
                        if args[0] == "~":
                            os.chdir(os.path.expanduser("~"))
                        else:
                            os.chdir(args[0])
                    except FileNotFoundError:
                        print(f"{args[0]}: No such file or directory")
                else:
                    print("cd: missing argument.")
            case _:
                
                if command.startswith("'") or command.startswith('"'):
                    os.system(command + " " + " ".join(args))
                    
                else:
                    command_path = self.getPathByCommandName(command)
                
                    if command_path:
                        os.system(command + " " + " ".join(args))
                    else:
                        print(f"{command}: command not found")
        return None

def main():
    terminal = shell()
    
    try:
        terminal.start()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
