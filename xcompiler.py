# xcompiler.py
import re
from xvm_core import XVM

# ================= AST =================
class Node: pass

class Program(Node):
    def __init__(self):
        self.statements = []

class VarAssign(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Print(Node):
    def __init__(self, expr):
        self.expr = expr

class If(Node):
    def __init__(self, cond):
        self.cond = cond
        self.body = []

class Loop(Node):
    def __init__(self, cond):
        self.cond = cond
        self.body = []

class Num(Node):
    def __init__(self, v):
        self.v = float(v)

class Var(Node):
    def __init__(self, n):
        self.n = n

class BinOp(Node):
    def __init__(self, l, op, r):
        self.l = l
        self.op = op
        self.r = r

# ================= TOKEN =================
def tokenize(expr):
    return re.findall(
        r'\d+\.\d+|\d+|NOT|==|!=|<=|>=|<|>|\+|-|\*|/|[A-Za-z_]\w*',
        expr
    )

# ================= PARSER =================
def parse_expr(expr):
    t = tokenize(expr)

    if len(t) == 1:
        return Num(t[0]) if t[0][0].isdigit() else Var(t[0])

    if len(t) == 3:
        return BinOp(parse_expr(t[0]), t[1], parse_expr(t[2]))

    cur = parse_expr(t[0])
    i = 1
    while i < len(t):
        cur = BinOp(cur, t[i], parse_expr(t[i+1]))
        i += 2
    return cur

def parse_x(lines):
    prog = Program()
    stack = [prog]

    for line in lines:
        line = line.strip()
        if not line: continue
        if line.endswith(";"): line = line[:-1]

        cur = stack[-1]
        target = cur.statements if isinstance(cur, Program) else cur.body

        if line.startswith("print("):
            target.append(Print(parse_expr(line[6:-1])))

        elif line.startswith("if "):
            node = If(parse_expr(line[3:].rstrip("{")))
            target.append(node)
            stack.append(node)

        elif line.startswith("loop "):
            node = Loop(parse_expr(line[5:].rstrip("{")))
            target.append(node)
            stack.append(node)

        elif line == "}":
            if len(stack) == 1:
                raise ValueError("unmatched '}'")
            stack.pop()

        elif "=" in line:
            v, e = line.split("=", 1)
            target.append(VarAssign(v.strip(), parse_expr(e.strip())))

        else:
            raise ValueError("syntax error: " + line)

    if len(stack) != 1:
        raise ValueError("block not closed")

    return prog

# ================= CODEGEN =================
OPMAP = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "/": "DIV",
    "==": "EQ",
    "!=": "NEQ",
    "<": "LT",
    ">": "GT",
    "<=": "LE",
    ">=": "GE",
    "NOT": "NEQ"   # ★ 핵심 수정: NOT = !=
}

def emit(node, bc):
    if isinstance(node, Program):
        for s in node.statements:
            emit(s, bc)

    elif isinstance(node, VarAssign):
        emit(node.expr, bc)
        bc.append(f"STORE {node.name}")

    elif isinstance(node, Print):
        emit(node.expr, bc)
        bc.append("PRINT")

    elif isinstance(node, Num):
        bc.append(f"PUSH_NUM {node.v}")

    elif isinstance(node, Var):
        bc.append(f"LOAD {node.n}")

    elif isinstance(node, BinOp):
        emit(node.l, bc)
        emit(node.r, bc)
        bc.append(OPMAP[node.op])

    elif isinstance(node, If):
        emit(node.cond, bc)
        j = len(bc)
        bc.append("JMP_IF_FALSE 0")
        for s in node.body:
            emit(s, bc)
        bc[j] = f"JMP_IF_FALSE {len(bc)}"

    elif isinstance(node, Loop):
        start = len(bc)
        emit(node.cond, bc)
        j = len(bc)
        bc.append("JMP_IF_FALSE 0")
        for s in node.body:
            emit(s, bc)
        bc.append(f"JMP {start}")
        bc[j] = f"JMP_IF_FALSE {len(bc)}"

def compile_x(path):
    with open(path) as f:
        prog = parse_x(f.readlines())
    bc = []
    emit(prog, bc)
    return bc

def save_xbin(bc, out):
    open(out, "w").write("\n".join(bc))

def pack_xrun(xbin, out):
    code = open(xbin).read().splitlines()
    open(out, "w").write(
        "from xvm_core import XVM\n"
        f"vm=XVM({code})\n"
        "vm.run()\n"
    )
