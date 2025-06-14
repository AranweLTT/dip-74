; Padovan sequence
; X: P(n-3)
; Y: P(n-2)
; Z: P(n-1)
; R: P(n), scratch

; Initial state
org 0
    add 1 y
    mov y z
    mov y r

; Compute next number
org 3
    ; Shift
    mov r x ; P(n-3) < P(n-2) (from scratch)
    mov y r ; output previous result
    mov z y ; P(n-2) < P(n-1)
    mov r z ; P(n-1) < P(n)
    mov y r ; P(n-2) in scratch

    ; Handle overflow
    jcc 11
    add 0 y
    ldx 2

    ; Compute next number !
    add 0 y

    ; Modulo 14
    ldx 2
    jcc 15
    add 0 y

; Finish up
org 15
    jcc 3
