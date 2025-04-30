import sys
import os
import shlex  # Import shlex for better command parsing
import subprocess

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
        
        """Execute a command with redirect arguments."""
        if any(op in args for op in ('>', '1>', '2>','>>', '1>>','2>>')):
            self.handle_redirect(command, args)
            return None
        
        """Executing the other commands"""
        match command:
            case "exit":
                if len(args) > 0 and args[0] == "0":
                    return 0
            case "echo":
                print(" ".join(args))
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
                # print('command',command)
                # print('args',args)
                
                

                                        
                command_path = self.getPathByCommandName(command)
                # print('command_path',command_path)
                                
                if command_path:
                    # Use subprocess to handle more complex command execution
                    subprocess.run([command] + args, check=True)
                    # os.exe(command_path, [command] + args)
                
                    
                    
                else:
                    print(f"{command}: command not found")
        return None
    
    
    def handle_redirect(self,command, args):
        """Handle output redirection."""
        
        # Check for output redirection operators

        
        redirection_ops = {'>': 'w', '1>': 'w', '2>': 'w', '>>': 'a', '1>>': 'a','2>>': 'a'}
        for op, mode in redirection_ops.items():
            if op in args:
                index = args.index(op)
                output_file = args[index + 1]
                with open(output_file, mode) as f:
                    subprocess.run([command] + args[:index], stdout=f if '2' not in op else None, stderr=f if '2' in op else None)
                    break

def main():
    terminal = shell()
    
    try:
        terminal.start()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
