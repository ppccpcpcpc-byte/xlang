# xvm_core.py
class XVM:
    def __init__(self, bytecode):
        self.bytecode = bytecode
        self.pc = 0
        self.stack = []
        self.vars = {}

    def run(self):
        while self.pc < len(self.bytecode):
            instr = self.bytecode[self.pc]
            parts = instr.split()

            if parts[0] == "PUSH_NUM":
                self.stack.append(float(parts[1]))
            elif parts[0] == "PUSH_STR":
                val = instr.split('"')[1]
                self.stack.append(val)
            elif parts[0] == "STORE":
                self.vars[parts[1]] = self.stack.pop()
            elif parts[0] == "LOAD":
                self.stack.append(self.vars.get(parts[1], 0))
            elif parts[0] == "ADD":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a + b)
            elif parts[0] == "SUB":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a - b)
            elif parts[0] == "MUL":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a * b)
            elif parts[0] == "DIV":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a / b)
            elif parts[0] == "EQ":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a == b)
            elif parts[0] == "NEQ":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a != b)
            elif parts[0] == "LT":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a < b)
            elif parts[0] == "GT":
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a > b)
            elif parts[0] == "NOT":
                val = self.stack.pop(); self.stack.append(not val)
            elif parts[0] == "PRINT":
                print(self.stack.pop())
            elif parts[0] == "JMP":
                self.pc = int(parts[1]) - 1
            elif parts[0] == "JMP_IF_FALSE":
                val = self.stack.pop()
                if not val:
                    self.pc = int(parts[1]) - 1
            self.pc += 1
