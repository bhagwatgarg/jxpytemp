extern malloc

section	.data

_temp1	dd	0
_temp2	dd	0
_temp3	dd	0
_temp5	dd	0
_temp6	dd	0
_temp4	dd	0

section .text
	global main
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 56
	mov rax, qword [rbp+16]
	mov rsp, rbp
	pop rbp
	ret
main2$Main$int$int:
	push rbp
	mov rbp, rsp
	sub rsp, 56
	mov rax, 22
	mov [rbp-32], rax
	mov rax, qword [rbp-32]
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
	mov rax, 2
	mov rbx, rax
	imul rbx, rax
	mov rcx, rbx
	add rcx, rax
	mov rdx, rcx
	sub rdx, rax
	mov rax, [rbp-8]
	mov [rbp-48], rdx
	push qword [rbp-48]
	push qword [rbp-48]
	push rax
	call main2$Main$int$int
	add rsp, 24
	mov [rbp-56], rax
	mov rax, 1
	mov rsp, rbp
	pop rbp
	ret
