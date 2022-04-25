default rel

extern malloc

extern printf

extern scanf

section	.data

pint: db	"%ld ", 0
neg_: db "-"
sint: db	"%ld", 0
_temp1	dd	0
_temp2	dd	0
_temp4	dd	0
_temp3	dd	0
_temp5	dd	0
_temp7	dd	0
_temp6	dd	0
_temp8	dd	0
_temp10	dd	0
_temp9	dd	0
_temp11	dd	0
_temp13	dd	0
_temp12	dd	0

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
    mov ebx, 1               ; fd = STDOUT_FILENO
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
    mov    edi, 1               ; fd = STDOUT_FILENO
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
	sub rsp, 200
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 200
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
	sub rsp, 200
	mov rax,0
	push rax
	call malloc
	mov [rbp -40 ], rax
	add rsp, 8
	push rax
	call Imports$Imports
	add rsp, 8
	mov  rbx, 5
	mov  rcx, 6
	mov  rdx, 7
	mov qword [rbp-40], rax
	mov qword [rbp-48], rbx
	mov qword [rbp-56], rcx
	mov qword [rbp-64], rdx
	push qword [rbp-48]
	push rax
	call print$Imports$int
	add rsp, 16
	mov  rbx, 0
	mov  rcx, 0
	mov qword [rbp-80], rcx
for_$n_2:
	mov rax, qword [rbp-80]
	cmp rax, 10
	jl $n_1
	mov rax, 0
	jmp $n_2
$n_1:
	mov rax, 1
$n_2:
	mov rbx, rax
	cmp rbx, 0
	je for_$n_5
	jmp for_$n_4
for_$n_3:
	mov  rax, qword [rbp-80]
	mov rbx, rax
	add rbx, 1
	mov qword [rbp-80], rax
	mov qword [rbp-80], rbx
	jmp for_$n_2
for_$n_4:
	mov  rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push qword [rbp-80]
	push rax
	call print$Imports$int
	add rsp, 16
	mov  rbx, qword [rbp-80]
	mov qword [rbp-48], rbx
	mov qword [rbp-80], rbx
	jmp for_$n_3
for_$n_5:
	mov  rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push qword [rbp-48]
	push rax
	call print$Imports$int
	add rsp, 16
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
