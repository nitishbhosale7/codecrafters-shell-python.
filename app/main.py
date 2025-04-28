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
            
            if command == "exit 0":
                break
        
            print(f"{command}: command not found")
        
        return 0;
            
            

def main():
    
    terminal = shell()
    
    terminal.start()
    


if __name__ == "__main__":
    main()
 