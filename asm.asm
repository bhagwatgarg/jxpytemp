extern malloc

section	.data

_temp1	dd	0
_temp3	dd	0
_temp2	dd	0

section .text
	global main
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 40
main2$Main$int$int:
	push rbp
	mov rbp, rsp
	sub rsp, 40
	mov rax, 22
	mov [ebp-32], rax
	mov rax, qword [ebp-32]
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
	pop rbp 
	push rax 
	call Main$Main 
	add rsp, 8 
	push rax 
	call main$Main 
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
	call Main$Main
	add rsp, 8
	push rax
	call main$Main
	add rsp, 8
	mov rax, 1
	mov rsp, rbp
	pop rbp
	ret
