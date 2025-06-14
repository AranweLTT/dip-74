import sys
import re
from collections import namedtuple

# Config
debug = False
outreg = 'x'
simsteps = 15000


def format_listing(code):
    asm = ["nop x"]*16
    pc = 0
    for line in code:
        clean = line.lower().lstrip().rstrip('\n')
        fields = clean.split()
        if len(fields) > 0 and clean[0] != ';':
            instruction = instruction_regex.fullmatch(clean)
            if instruction["cmd"]=="org":
                pc = int(instruction["arg1"])
            else:
                asm[pc] = clean.split(";")[0].rstrip()
                pc = (pc+1)%16
    return asm


def print_listing(listing, program, printer=print):
    """ Prints machine code listing in binary with line numbers """
    line = 0
    for instruction in listing:
        op = instruction_regex.fullmatch(program[line].lstrip())
        if op["arg2"] is None:
            printer(f"{line:02d} {int(instruction):06b} {op['cmd']} {op['arg1']}")
        else:
            printer(f"{line:02d} {int(instruction):06b} {op['cmd']} {op['arg1']} {op['arg2']}")
        line += 1


# --- Assembler
instruction_regex = re.compile(r"(?P<cmd>org|nop|add|mov|jcc|ldx) +(?P<arg1>x|y|z|r|\d{1,9})(?: +(?P<arg2>x|y|z|r))? *(?:;.*)?")

def reg_addr(reg)->int:
    """ Returns address of register character """
    match reg:
        case 'x':
            return 0
        case 'y':
            return 1
        case 'z':
            return 2
        case 'r':
            return 3
        case _:
            raise Exception("Unrecognized register name")


def assembler(code, printer=print):
    """ Assembly text to machine code instructions. """
    program = [0x30]*16
    pc = 0
    for line in code:
        fields = line.split()
        if len(fields) > 0 :
            # Get instruction
            instruction = instruction_regex.fullmatch(line)
            match instruction["cmd"], instruction["arg1"], instruction["arg2"]:
                case "org", arg, None:
                    pc = int(arg)%16
                case "ldx", arg, None:
                    program[pc] = 0x00+int(arg)
                case "add", arg, dst:
                    program[pc] = 0X10+(int(arg)*4)+reg_addr(dst)
                case "jcc", arg, None:
                    program[pc] = 0X20+int(arg)
                case "mov", src, dst:
                    program[pc] = 0X30+(reg_addr(src)*4)+reg_addr(dst)
                case "nop", arg, None:
                    program[pc] = 0X30+(reg_addr(arg)*4)+reg_addr(arg)
                case _:
                    raise Exception("Unrecognized command")
            if instruction["cmd"] != "org": 
                pc += 1
    printer(f"ROM usage: {round((pc/16)*100)}% ({pc}/16)")
    return program[:pc]


# --- Simulator ---
State = namedtuple("State", "x, y, z, r, pc, program")

def build_starting_state(program)->State:
    """ Initial state all registers cleared """
    return State(0,0,0,0,0,program)


def step(state:State, result)->State:
    """ Run simulation step """
    x, y, z, r, pc, program = state
    if (x+y)>15:
        c = 1
    else:
        c = 0
    registers = [x, y, z, r]
    assert pc < len(program), "Program counter overflow."
    instruction = instruction_regex.fullmatch(program[pc])
    match instruction["cmd"], instruction["arg1"], instruction["arg2"]:
        case "ldx", arg, None:
            return State(int(arg)%16, y, z, r, (pc+1)%16, program)
        case "add", arg, dst:
            registers[reg_addr(dst)] = (x+y+int(arg))%16
            return State(registers[0], registers[1], registers[2], registers[3], (pc+1)%16, program)
        case "jcc", arg, None:
            if c==0:
                return State(x, y, z, r, int(arg)%16, program)
            else:
                return State(x, y, z, r, (pc+1)%16, program)
        case "mov", src, dst:
            registers[reg_addr(dst)] = registers[reg_addr(src)]
            if(dst == outreg):
                result.append(registers[0])
            return State(registers[0], registers[1], registers[2], registers[3], (pc+1)%16, program)
        case "nop", arg, None:
            return State(x, y, z, r, (pc+1)%16, program)
        case _:
            raise Exception("Unrecognized command")


def guess_seq_len(seq)->int:
    guess = 1
    max_len = int(round(len(seq) / 2))
    for x in range(2, max_len):
        if seq[0:x] == seq[x:2*x] :
            return x
    return guess


def simulator(program, nsteps:int=2000, printer=print):
    result = []
    state = build_starting_state(program)
    for _ in range(nsteps):
        state = step(state, result)
        x, y, z, r, pc, program = state
        if debug:
            printer(f"[pc,x,y,z,r] {pc}\t{x},{y},{z},{r}")

    # Result
    seq_len=guess_seq_len(result[32:-1])
    if seq_len>1:
        printer(f"Sequence period estimate: {seq_len}")
        printer(result[:seq_len+3])
    else:
        printer(result)


if __name__ == "__main__":
    # Get arguments
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <input_file>")
        sys.exit(1)
    else:
        input_file = sys.argv[1]
    
    # Load assembly file
    with open(input_file, 'r') as f:
        code = f.readlines()

    # Clean program
    asm = format_listing(code)
    # print(asm)

    # 1) Assemble program
    print("--- Assembler ---")
    listing = assembler(asm)
    print_listing(listing, asm)

    # 2) Simulate program
    print("\n--- Simulation ---")
    simulator(asm, simsteps)
