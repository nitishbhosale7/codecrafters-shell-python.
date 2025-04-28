import sys



class shell:
    def __init__(self):
        self.history = []
        
        
    def start(self):
        self.repl()
        
        
    def repl(self):
        while True:
            # Uncomment this block to pass the first stage
            sys.stdout.write("$ ")

            # Wait for user input
            command = input()
            
            self.history.append(command)
            
            initial_command = command.split(" ")[0]
            
            args = command.split(" ")[1:]
            
            if self.execute(initial_command,args) == 0:
                break
            
            
        
        
    
    def execute(self, command,args):
        # This function is a placeholder for executing commands
        # In a real shell, you would use subprocess or os.system to execute the command
        match command:
            case "exit":
                if len(args) > 0 and args[0] == "0":
                    return 0
            case "echo":
                print(" ".join(args))
                
            case "type":
                next_command = args[0]
                match next_command:
                    case "echo":
                        print("echo is a shell builtin")
                    case "exit":
                        print("exit is a shell builtin")
                    case "type":
                        print("type is a shell builtin")
                    case _:
                        print(f"{next_command} not found")
            case _:
                print(f"{command}: command not found")
            
            

def main():
    
    terminal = shell()
    
    try:
    
        terminal.start()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    


if __name__ == "__main__":
    main()
 