; Initial state
org 0
    ldx 1
    mov x r

; Compute next Fibonacci number
org 2
    mov r x ; load n-1 (x=r)
    mov r z ; save n-1 (z=r)

    ; Check overflow
    jcc 7
    add 0 y
    ldx 6

    ; Compute next number !
    add 0 y

    ; Modulo 10
    ldx 6
    jcc 12
    add 0 y

; Finish up
org 12
    mov y r ; output result
    mov z y ; load n-2 (y=z)
    ldx 0   ; force carry clear
    jcc 2   ; loop
