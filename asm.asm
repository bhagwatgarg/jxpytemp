extern malloc

extern printf

section	.data

pint: db	"%ld"
_temp1	dd	0
_temp2	dd	0
_temp3	dd	0
_temp4	dd	0
_temp6	dd	0
_temp5	dd	0

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
	sub rsp, 40
	mov rax, qword [rbp+16]
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 40
	mov rax, qword [rbp+16]
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
	sub rsp, 40
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
	mov rbx, 5
	mov rcx, rbx
	add rcx, rbx
	mov rdx, rcx
	add rdx, rbx
	mov rbx, qword [rbp+16]
	mov [rbp+16], rbx
	mov [rbp-32], rdx
	push qword [rbp-32]
	push rbx
	call print_int$Imports$int
	add rsp, 16
	mov rax, qword [rbp-32]
	mov rsp, rbp
	pop rbp
	ret
