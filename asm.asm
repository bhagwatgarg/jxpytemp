default rel

extern malloc

extern printf

extern scanf

section	.data

pint: db	"%ld ", 0
sint: db	"%ld", 0
_temp1	dd	0
_temp2	dd	0
_temp3	dd	0
_temp4	dd	0
_temp6	dd	0
_temp5	dd	0

section .text
	global main
print$Imports$int:	
	push rbp
	mov rbp, rsp
	push rsi
	push rdi
	mov rsi, qword [rbp+24]
	lea rdi, [rel pint]
	xor rax, rax
	call printf
	xor rax, rax
	pop rsi
	pop rdi
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
	sub rsp, 176
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 176
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
	sub rsp, 176
	mov rax,0
	push rax
	call malloc
	mov [rbp -40 ], rax
	add rsp, 8
	mov rsp, rbp
	pop rbp
	push rax
	call Imports$Imports
	add rsp, 8
	mov  rbx, 0
	mov  rcx, 0
	mov qword [rbp-40], rax
	mov qword [rbp-48], rcx
for_$n_2:
	mov rax, qword [rbp-48]
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
	mov rax, qword [rbp-48]
	add rax, 1
	mov qword [rbp-48], rax
	jmp for_$n_2
for_$n_4:
	mov  rax, qword [rbp-40]
	mov qword [rbp-40], rax
	push qword [rbp-48]
	push rax
	call print$Imports$int
	add rsp, 16
	jmp for_$n_3
for_$n_5:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
