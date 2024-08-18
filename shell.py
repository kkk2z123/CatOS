import os

class BasicInterpreter:
    def __init__(self):
        self.variables = {}
        self.lines = []
        self.line_numbers = {}
        self.current_line = 0

    def execute_line(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return  # Skip empty lines and comments

        if ' ' not in line:
            print(f"Unsupported line format: {line}")
            return

        # Extract line number and command
        parts = line.split(' ', 1)
        line_number = int(parts[0])
        command = parts[1] if len(parts) > 1 else ''

        self.line_numbers[line_number] = line

        if command.startswith("PRINT "):
            print(command[6:])
        elif command.startswith("LET "):
            try:
                var, expr = command[4:].split('=')
                var = var.strip()
                expr = expr.strip()
                self.variables[var] = eval(expr, {}, self.variables)
            except Exception as e:
                print(f"Error: {e}")
        elif command.startswith("INPUT "):
            try:
                var = command[6:].strip()
                self.variables[var] = input(f"{var} = ")
            except Exception as e:
                print(f"Error: {e}")
        elif command.startswith("IF "):
            self.handle_if(command[3:])
        elif command.startswith("GOTO "):
            self.handle_goto(command[5:])
        else:
            print(f"Unsupported BASIC command: {command}")

    def handle_if(self, condition):
        try:
            # Example: IF X > 10 GOTO 20
            parts = condition.split(' GOTO ')
            if len(parts) != 2:
                print(f"Invalid IF statement: {condition}")
                return
            condition_expr = parts[0].strip()
            goto_line = int(parts[1].strip())
            if eval(condition_expr, {}, self.variables):
                self.current_line = goto_line
        except Exception as e:
            print(f"Error: {e}")

    def handle_goto(self, line_number):
        try:
            self.current_line = int(line_number.strip())
        except Exception as e:
            print(f"Error: {e}")

    def run(self, filename):
        if not os.path.isfile(filename):
            print(f"File '{filename}' not found")
            return

        with open(filename, 'r') as file:
            lines = file.readlines()

        # Parse lines into a dictionary with line numbers
        self.lines = {}
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    line_number = int(parts[0])
                    command = parts[1].strip()
                    self.lines[line_number] = command

        # Sort lines by line number
        for line_number in sorted(self.lines):
            self.line_numbers[line_number] = self.lines[line_number]

        # Execute lines
        while self.current_line in self.line_numbers:
            line = self.line_numbers[self.current_line]
            self.execute_line(f"{self.current_line} {line}")
            self.current_line += 1

class SimpleShell:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.basic_interpreter = BasicInterpreter()

    def cd(self, path):
        if path == "..":
            parent_directory = os.path.dirname(self.current_directory)
            if parent_directory:
                os.chdir(parent_directory)
                self.current_directory = os.getcwd()
            else:
                print("Already at the root directory")
        else:
            try:
                os.chdir(path)
                self.current_directory = os.getcwd()
            except FileNotFoundError:
                print(f"Directory '{path}' not found")
            except NotADirectoryError:
                print(f"'{path}' is not a directory")
    def echo(self, args):
        if args:
            print(' '.join(args))  # 引数をスペースで結合して表示
        else:
            print("Usage: echo <text>")  # 引数がない場合の使い方メッセージ

    def date(self, args):
        now = datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))

    def mkdir(self, dir_name):
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            print(f"Directory '{dir_name}' already exists")
        except FileNotFoundError:
            print(f"Cannot create directory '{dir_name}'")

    def ls(self):
        try:
            files = os.listdir(self.current_directory)
            for file in files:
                print(file)
        except FileNotFoundError:
            print(f"Directory '{self.current_directory}' not found")

    def cal(self, args):
        try:
            import calendar
            from datetime import datetime

            if not args:
                year = datetime.now().year
                month = datetime.now().month
            elif len(args) == 1:
                month = int(args[0])
                year = datetime.now().year
            elif len(args) == 2:
                month = int(args[0])
                year = int(args[1])
            else:
                print("Usage: cal [month] [year]")
                return

            cal_text = calendar.month(year, month)
            print(cal_text)
        except ValueError:
            print("Invalid month or year")

    def basic(self, args):
        if not args:
            print("Usage: basic <filename>")
            return

        filename = args[0]
        self.basic_interpreter.run(filename)

    def run(self):
        while True:
            command = input(f"{self.current_directory} >>> ")
            parts = command.split()
            if parts:
                cmd = parts[0].lower()
                args = parts[1:]

                if cmd == "exit":
                    break
                elif cmd == "cd":
                    self.cd(' '.join(args))
                elif cmd == "mkdir":
                    self.mkdir(' '.join(args))
                elif cmd == "ls":
                    self.ls()
                elif cmd == "cal":
                    self.cal(args)
                elif cmd == "basic":
                    self.basic(args)
                elif cmd == "date":
                    self.date(args)
                elif cmd == "echo":
                    self.echo(args)
                else:

                    print("Unknown command. Available commands: cd, mkdir, ls, cal, basic,echo,date,exit")

if __name__ == "__main__":
    shell = SimpleShell()
    shell.run()
