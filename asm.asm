extern malloc

extern printf

section	.data

pint: db	"%ld"
_temp1	dd	0
_temp2	dd	0
_temp4	dd	0
_temp5	dd	0
_temp3	dd	0
_temp6	dd	0
_temp8	dd	0
_temp9	dd	0
_temp7	dd	0
_temp10	dd	0
_temp12	dd	0
_temp11	dd	0

section .text
	global main
print_int$Imports$int:	
	push rbp
	mov rbp, rsp
	push rsi
	push rdi
	mov rsi, qword [rbp+24]
	mov rdi, pint
	call printf
	pop rsi
	pop rdi
	mov rsp, rbp
	pop rbp
	ret
Imports$Imports:
	push rbp
	mov rbp, rsp
	sub rsp, 56
	mov rax, qword [rbp-16]
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 56
	mov rax, qword [rbp-16]
	mov rsp, rbp
	pop rbp
	ret
rec$Main$int:
	push rbp
	mov rbp, rsp
	sub rsp, 56
	mov rax, qword [rbp-40]
	cmp rax, 5
	jg $n_1
	mov rax, 0
	jmp $n_2
$n_1:
	mov rax, 1
$n_2:
	mov rbx, rax
	cmp rbx, 0
	je if1_$n_3
if1_$n_2:
	mov rax, qword [rbp-40]
	mov rsp, rbp
	pop rbp
	ret
if1_$n_3:
	mov rax, qword [rbp-40]
	add rax, 1
	mov rbx , [rbp-8]
	mov [rbp-72], rax
	push qword [rbp-72]
	push rbx
	call rec$Main$int
	add rsp, 16
	mov [rbp-80], rax
	mov rax, qword [rbp-80]
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
	sub rsp, 56
	mov rax,0
	push rbp
	mov rbp, rsp
	push rax
	call malloc
	add rsp, 8
	mov rsp, rbp
	pop rbp
	push rax
	call Imports$Imports
	add rsp, 8
	mov rbx, 0
	mov rcx, 0
	mov rdx, 3
	mov rsi, 2
	mov rdi , [rbp-8]
	mov [rbp-96], rbx
	mov [rbp-104], rcx
	mov [rbp-112], rdx
	mov [rbp-120], rsi
	push qword [rbp-104]
	push rdi
	call rec$Main$int
	add rsp, 16
	mov rbx, qword [rbp-16]
	mov [rbp-128], rax
	mov [rbp-16], rbx
	push qword [rbp-128]
	push rbx
	call print_int$Imports$int
	add rsp, 16
	mov rax, qword [rbp-96]
	mov rsp, rbp
	pop rbp
	ret
