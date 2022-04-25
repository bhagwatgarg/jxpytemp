default rel

extern malloc

extern printf

extern scanf

section	.data

pint: db	"%ld ", 0
neg_: db "-"
sint: db	"%ld", 0
_temp1	dd	0
_b$main$Main	dd	0
_temp2	dd	0
_temp3	dd	0
_temp4	dd	0
_temp5	dd	0
_temp6	dd	0
_temp7	dd	0
_temp8	dd	0
_temp9	dd	0
_temp10	dd	0
_temp11	dd	0
_temp12	dd	0
_temp13	dd	0
_temp14	dd	0
_temp15	dd	0
_temp16	dd	0
_temp17	dd	0
_temp18	dd	0
_temp19	dd	0
_temp20	dd	0
_temp21	dd	0
_temp22	dd	0
_temp23	dd	0
_temp24	dd	0
_temp25	dd	0
_temp26	dd	0
_temp27	dd	0
_temp28	dd	0
_temp29	dd	0
_temp30	dd	0
_temp32	dd	0
_temp31	dd	0
_temp33	dd	0
_temp35	dd	0
_temp34	dd	0
_temp36	dd	0
_temp38	dd	0
_temp37	dd	0
_temp39	dd	0
_temp41	dd	0
_temp40	dd	0
_temp42	dd	0
_temp44	dd	0
_temp43	dd	0
_temp45	dd	0
_temp47	dd	0
_temp46	dd	0
_temp48	dd	0
_temp50	dd	0
_temp49	dd	0
_temp51	dd	0
_temp53	dd	0
_temp52	dd	0

section .text
	global main
print_uint32:
    mov    eax, edi              ; function arg
    cmp eax, 0
    jge print_uint32_c
    xor eax, 0xFFFFFFFF
    add eax, 1
    push rax
    mov eax, 4               ; __NR_write from /usr/include/asm/unistd_64.h
    mov ebx, 1               ; fd = STDdest_FILENO
    mov ecx, neg_
    mov edx, 1
    int 80h
    pop rax

print_uint32_c:

    mov    ecx, 0xa              ; base 10
    push   rcx                   ; ASCII newline
    mov    rsi, rsp
    sub    rsp, 16               ; not needed on 64-bit Linux, the red-zone is big enough.  Change the LEA below if you remove this.

;;; rsi is pointing at nl on the stack, with 16B of allocated space below that.
.toascii_digit:                ; do {
    xor    edx, edx
    div    ecx                   ; edx=remainder = low digit = 0..9.  eax/=10
                                 ;; DIV IS SLOW.  use a multiplicative inverse if performance is relevant.
    add    edx, '0'
    dec    rsi                 ; store digits in MSD-first printing order, working backwards from the end of the string
    mov    [rsi], dl

    test   eax,eax             ; } while(x);
    jnz  .toascii_digit
;;; rsi points to the first digit


    mov    eax, 1               ; __NR_write from /usr/include/asm/unistd_64.h
    mov    edi, 1               ; fd = STDdest_FILENO
    ; pointer already in RSI    ; buf = last digit stored = most significant
    lea    edx, [rsp+16 + 1]    ; yes, its safe to truncate pointers before subtracting to find length.
    sub    edx, esi             ; RDX = length = end-start, including the
    syscall                     ; write(1, string RSI,  digits + 1)

    add  rsp, 24                ; (in 32-bit: add esp,20) undo the push and the buffer reservation
    ret



print$Imports$int:	
	push rbp
	mov rbp, rsp

	push rsi
	push rdi
	push rax
	push rbx
	push rcx
	push rdx
	mov rdi, qword [rbp+24] 

	call print_uint32

	pop rdx
	pop rcx
	pop rbx
	pop rax
	pop rdi
	pop rsi

	mov rsp, rbp
	pop rbp
	ret
scan_int$Imports:
	push rbp
	mov rbp, rsp
	push rsi
	push rdi
	add rsp, 8
	mov rsi, rsp
	lea rdi, [rel sint]
	xor rax, rax
	call scanf
	mov rax, qword [rsp]
	pop rdi
	pop rsi
	mov rsp, rbp
	pop rbp
	ret
        
Imports$Imports:
	push rbp
	mov rbp, rsp
	sub rsp, 328
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 328
	mov rsp, rbp
	pop rbp
	ret
main:
	mov rax,0 
	push rbp 
	mov rbp, rsp 
	push rax 
	call malloc 
	add rsp, 8 
	mov rsp, rbp 
	push rax 
	call Main$Main 
	add rsp, 8 
	push rax 
	call main$Main 
	add rsp, 8 
	pop rbp 
	ret
main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 328
	mov rax,0
	push rax
	call malloc
	mov [rbp -40 ], rax
	add rsp, 8
	push rax
	call Imports$Imports
	add rsp, 8
	mov qword rbx, 5
	mov qword rcx, 6
	mov qword rdx, 7
	mov qword rsi, 5
	mov qword rdi, 23
	mov qword [rbp-80], 3
	mov qword [rbp-88], 4
	mov qword [rbp-96], 5
	mov qword [rbp-48], rbx
	mov rbx, 5
	sub rbx, 1
	add rbx, 6
	sub rbx, 2
	add rbx, 7
	sub rbx, 3
	add rbx, 8
	add rbx, 9
	add rbx, 10
	add rbx, 5
	sub rbx, 1
	add rbx, 6
	sub rbx, 2
	add rbx, 7
	sub rbx, 3
	add rbx, 8
	add rbx, 9
	add rbx, 10
	add rbx, 5
	sub rbx, 1
	add rbx, 6
	sub rbx, 2
	add rbx, 7
	sub rbx, 3
	add rbx, 8
	add rbx, 9
	add rbx, 10
	mov qword [rbp-112], 23
	mov qword [rbp-120], 3
	mov qword [rbp-128], 4
	mov qword [rbp-136], 5
	mov qword [rbp-144], 0
	mov qword [rbp-40], rax
	mov qword [rbp-104], rbx
	mov qword [rbp-56], rdx
	mov qword [rbp-64], rsi
	mov qword [rbp-72], rdi
for_$n_2:
	mov rax, qword [rbp-144]
	cmp rax, 4
	jl $n_1
	mov rax, 0
	jmp $n_2
$n_1:
	mov rax, 1
$n_2:
	cmp rax, 0
	je for_$n_5
	jmp for_$n_4
for_$n_3:
	mov rax, qword [rbp-144]
	add rax, 1
	mov qword [rbp-144], rax
	jmp for_$n_2
for_$n_4:
	mov qword rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push rax
	call scan_int$Imports
	add rsp, 8
	mov qword rbx, qword [rbp-40]
	mov qword [rbp-200], rax
	mov qword [rbp-40], rbx
	push qword [rbp-200]
	push rbx
	call print$Imports$int
	add rsp, 16
	jmp for_$n_3
for_$n_5:
	mov qword rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push qword [rbp-72]
	push rax
	call print$Imports$int
	add rsp, 16
	mov qword rbx, qword [rbp-40]
	mov qword [rbp-40], rbx
	push qword [rbp-104]
	push rbx
	call print$Imports$int
	add rsp, 16
	mov qword rbx, qword [rbp-40]
	mov qword [rbp-40], rbx
	push qword [rbp-48]
	push rbx
	call print$Imports$int
	add rsp, 16
	mov qword rbx, 0
	mov qword rcx, 0
	mov qword [rbp-216], rcx
for_$n_7:
	mov rax, qword [rbp-216]
	cmp rax, 10
	jl $n_3
	mov rax, 0
	jmp $n_4
$n_3:
	mov rax, 1
$n_4:
	cmp rax, 0
	je for_$n_10
	jmp for_$n_9
for_$n_8:
	mov qword rax, qword [rbp-216]
	mov rbx, rax
	add rbx, 1
	mov qword [rbp-216], rax
	mov qword [rbp-216], rbx
	jmp for_$n_7
for_$n_9:
	mov qword rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push qword [rbp-216]
	push rax
	call print$Imports$int
	add rsp, 16
	mov qword rbx, qword [rbp-216]
	mov qword [rbp-48], rbx
	mov qword [rbp-216], rbx
	jmp for_$n_8
for_$n_10:
	mov qword rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push qword [rbp-48]
	push rax
	call print$Imports$int
	add rsp, 16
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
