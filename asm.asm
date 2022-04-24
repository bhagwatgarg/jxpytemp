extern malloc

extern printf

section	.data

pint: db	"%ld"
_temp1	dd	0
_temp2	dd	0
_temp3	dd	0
_temp4	dd	0
_temp5	dd	0
_temp6	dd	0
_temp7	dd	0
_temp8	dd	0
_temp9	dd	0
_temp11	dd	0
_temp10	dd	0

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
	sub rsp, 224
	mov rax, qword [rbp-16]
	mov rsp, rbp
	pop rbp
	ret
func$Main$int:
	push rbp
	mov rbp, rsp
	sub rsp, 224
	mov rax, qword [rbp-32]
	imul rax, qword [rbp-32]
	mov rbx, rax
	add rbx, 1
	mov [rbp-32], rax
	mov [rbp-40], rbx
	mov rax, qword [rbp-40]
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 224
	mov rax, qword [rbp-16]
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
	sub rsp, 224
	mov rax,0
	push rax
	call malloc
	add rsp, 8
	mov rsp, rbp
	pop rbp
	push rax
	call Imports$Imports
	add rsp, 8
	mov rbx, 0
	mov rcx, 1
	mov rdx, 0
	mov [rbp-64], rbx
	mov [rbp-72], rcx
	mov [rbp-80], rdx
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
	je for_$n_8
	jmp for_$n_4
for_$n_3:
	mov rax, qword [rbp-80]
	add rax, 1
	mov [rbp-80], rax
	jmp for_$n_2
for_$n_4:
	mov rax, qword [rbp-72]
	add rax, 1
	mov rbx, rax
	cmp rbx, 5
	jg $n_3
	mov rbx, 0
	jmp $n_4
$n_3:
	mov rbx, 1
$n_4:
	mov rcx, rbx
	mov [rbp-72], rax
	cmp rcx, 0
	je if1_$n_7
	jmp if1_$n_6
if1_$n_6:
	jmp for_$n_3
if1_$n_7:
	mov rax, qword [rbp-64]
	add rax, 1
	mov [rbp-64], rax
	jmp for_$n_3
for_$n_8:
	mov rax, qword [rbp-16]
	mov [rbp-16], rax
	push qword [rbp-72]
	push rax
	call print_int$Imports$int
	add rsp, 16
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
