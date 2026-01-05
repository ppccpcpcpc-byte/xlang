# xlang
**its a dev's language.**

## waht the xlang?
X Language & XVM
X is a lightweight custom programming language designed to run on its own virtual machine, XVM.
It follows a clear separation between compiler (brain) and virtual machine (heart).
Overview
Pipeline
코드 복사

X source (.x)
   ↓
X Compiler
   ↓
XVM bytecode (.xbin / .xrun)
   ↓
XVM (Virtual Machine)
.x files are human-readable source code
.xbin / .xrun are binary files, not text
Execution is handled only by XVM, not Python itself
Key Concepts
Compiler ≠ Interpreter
X is a compiled language
XVM executes binary bytecode
.xrun files may contain null bytes (this is normal)
⚠️ Do NOT run .xrun files with python file.xrun
Always execute them through XVM
Features
Variables and assignment
if statements
loop statements
Nested control flow
Numeric operations
String literals (" " or ' ')
Binary-safe execution
Example (X Source)
```
X
i = 1;

loop i < 5 {
    print(i);
    i = i + 1;
}

x = 10;
y = 20;

if x + y == 30 {
    print(x + y);
}
```
Compilation

```Python
import xvm

vm = xvm.VM()
vm.load_bin("test.xrun")
vm.run()
```
❌ Incorrect (will fail)
Bash
python test.xrun
This will cause:

Running binaries as Python source is the bug.
Project Structure


├── xcompiler.py     # X language compiler
├── xvm.py / xvm_core.py  # X Virtual Machine
├── examples/
│   └── test.x
├── README.md


|xlang|py|
|:----|:----|
|print()|print()|
|fun() {}|def|
|i=8|i=8|

`print()`
Design Philosophy
Clear separation of responsibility
Minimal magic
VM-first execution model
No silent behavior
Status
Compiler: stable
XVM: stable
