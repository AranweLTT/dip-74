<!-- Template from https://github.com/othneildrew/Best-README-Template -->
<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<div align="center">
  <h2 align="center">Single board DIP-switch programmable 4-bit CPU from discrete 74-series logic</h2>
</div>


Inspired by the TD4—a discrete 4‑bit CPU initially presented in Iku Watanabe's <i>How to Build a CPU</i>—this project delivers a fully revisited custom-designed, paper‑programmable board built entirely from 74‑series logic ICs. It requires no host computer, uses modern, easily sourced components (no obscure new-old ebay chips), facilitating both educational usage as well as allowing more advanced tinkering. The design features a four-instruction architecture, four general-purpose registers, and 16 words of 6-bit program memory set via DIP switches.

![board]


<!-- TABLE OF CONTENTS -->
<summary>Table of Contents</summary>
<ol>
  <li><a href="#leaderboard">Leaderboard</a></li>
  <li><a href="#getting-started">Getting started</a></li>
  <li><a href="#architecture">Architecture</a></li>
  <li><a href="#program-example">Program example</a></li>
  <li><a href="#references">References</a></li>
  <li><a href="#licence">Licence</a></li>
</ol>


<!-- LEADERBOARD -->
## Leaderboard

| Rank | Sequence Length  | User     | Sequence Name            | Assembly file                                 |
|------|------------------|----------|--------------------------|-----------------------------------------------|
| 1    | 336              | aranweltt  | Modular Padovan Sequence | [software/padovan.asm](software/padovan.asm)  |

<u>Leaderboard rules:</u>
- Valid sequences: to be eligible, the sequence must contain at least 100 computed elements that are consecutivelly output to a single register of your choice. Externally timed/manual inputs are not allowed. Longer sequences will rank higher on the leaderboard.
- Verification: submissions must be reproducible and testable. Your program should run successfully on both the Python simulator and in Logisim, and it will be tested on the actual hardware before being accepted.
- Code requirements: clear comments are preferred to aid review and help others understand your approach. Please include a brief explanation of your algorithm in the description field.
- Submission: Submit your entry through the following form: [Submission Form](https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAANAAUIfpdFUQUtSQks1OVhKVEpGSFY4Uk1IQ0NHWUpTNi4u). You’ll need to provide your program source (.asm), the expected output sequence and it's length, and a brief explanation.


<!-- GETTING STARTED -->
## Getting started
Start by cloning this repository.

```sh
git clone 'https://github.com/AranweLTT/dip-74.git'
```

To use the assembler and simulator write a program in a .asm file and run the simulator specifying the file.

```sh
python assembler.py <input_file> 
```

At the top of the Python file some parameters can be adjusted such as the target output register, which will be used to get the output sequence and its length. A debug mode can also be enabled to display the cpu state cycle by cycle.


<!-- ARCHITECTURE -->
## Architecture
At its core, the CPU features four general‑purpose 4‑bit registers, doubling the TD4’s original count. Instructions are encoded in 6 bits: a 2‑bit opcode and 4 bits of operand/address data. Four primary operations are supported: immediate load into register X (LDX), register‑to‑register addition (ADD), conditional jumps on carry (JCC), and register moves (MOV).

| Mnemonic | Description                  | Opcode   | Description              |
|----------|------------------------------|----------|--------------------------|
| LDX      | Load value to register X     | 00DDDD   | X = DDDD                 |
| ADD      | Add registers X and Y        | 01SSDD   | DD = X+Y                 |
| JCC      | Jump if carry is clear       | 10AAAA   | PC = AAAA when carry = 0 |
| MOV      | Copy one register to another | 11SSDD   | DD = SS                  |

Each register is given a 2-bit address to designate it as a source (SS) or destination (DD) for a given operation. The addressing is as follows:

| Register | Address | Description                                         |
|----------|---------|-----------------------------------------------------|
| X        | 00      | Input to adder, capable of immediate loads.         |
| Y        | 01      | Input to adder.                                     |
| Z        | 10      | General purpose.                                    |
| R        | 11      | General purpose, usually used as a **R**esult register. |


<!-- PROGRAM EXAMPLE -->
## Program example
Modular Fibonacci example assembly program:
```armasm
; Initial state
ldx 1
mov x r

; Fibonacci
mov r x ; x=r
add 0 r ; Compute next number
mov x y ; y=x
ldx 0   ; force carry clear
jcc 2   ; loop
```

Assembler output:
```sh
--- Assembler ---
ROM usage: 44% (7/16)
00 000001 1
01 110011 51
02 111100 60
03 010011 19
04 110001 49
05 000000 0
06 100010 34
```

Simulator output:
```sh
--- Simulation ---
[pc :: x,y,z,r] 1 :: 1,0,0,0
[pc :: x,y,z,r] 2 :: 1,0,0,1
[pc :: x,y,z,r] 3 :: 1,0,0,1
[pc :: x,y,z,r] 4 :: 1,0,0,1
[pc :: x,y,z,r] 5 :: 1,1,0,1
[pc :: x,y,z,r] 6 :: 0,1,0,1
[pc :: x,y,z,r] 2 :: 0,1,0,1
[pc :: x,y,z,r] 3 :: 1,1,0,1
[pc :: x,y,z,r] 4 :: 1,1,0,2
[pc :: x,y,z,r] 5 :: 1,1,0,2
[pc :: x,y,z,r] 6 :: 0,1,0,2
[pc :: x,y,z,r] 2 :: 0,1,0,2
[pc :: x,y,z,r] 3 :: 2,1,0,2
[pc :: x,y,z,r] 4 :: 2,1,0,3
[pc :: x,y,z,r] 5 :: 2,2,0,3
[pc :: x,y,z,r] 6 :: 0,2,0,3
[pc :: x,y,z,r] 2 :: 0,2,0,3
[pc :: x,y,z,r] 3 :: 3,2,0,3
[pc :: x,y,z,r] 4 :: 3,2,0,5
```

<u>Logisim simulaiton:</u> (not the full sequence)
![data-path]


<!-- REFERENCES -->
## References
Project featuring the original TD4 architecture: [https://github.com/johnsonwust/TD4-4BIT-CPU](https://github.com/johnsonwust/TD4-4BIT-CPU)

Showcase from Philip Zucker: [https://www.philipzucker.com/td4-4bit-cpu/](https://www.philipzucker.com/td4-4bit-cpu/)


<!-- LICENCE -->
## Licence
[![License: GPL v3][gpl3-badge]][gpl3-url]

This work is licensed under a GNU GPL v3 licence.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python]: images/badge/python.svg
[github]: images/badge/github.svg
[github-url]: https://github.com
[gpl3-url]: https://www.gnu.org/licenses/gpl-3.0
[gpl3-badge]: https://img.shields.io/badge/License-GPLv3-blue.svg
[board]: images/board-top-2.png
[data-path]: simulation/logisim/output.gif
