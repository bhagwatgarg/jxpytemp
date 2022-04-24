default rel

extern malloc

extern printf

extern scanf

section	.data

pint: db	"%ld ", 0
sint: db	"%ld", 0
_temp1	dd	0
_temp2	dd	0
_temp4	dd	0
_temp5	dd	0
_temp3	dd	0
_temp6	dd	0
_temp7	dd	0
_temp8	dd	0
_temp9	dd	0
_temp11	dd	0
_temp12	dd	0
_temp10	dd	0
_temp13	dd	0
_temp14	dd	0
_temp16	dd	0
_temp17	dd	0
_temp15	dd	0
_temp18	dd	0
_temp20	dd	0
_temp19	dd	0
_temp21	dd	0
_temp23	dd	0
_temp22	dd	0
_temp24	dd	0
_temp26	dd	0
_temp25	dd	0

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
	pop rsi
	pop rdi
	mov rsp, rbp
	pop rbp
	ret
        
Imports$Imports:
	push rbp
	mov rbp, rsp
	sub rsp, 280
	mov rsp, rbp
	pop rbp
	ret
fact$Main$int:
	push rbp
	mov rbp, rsp
	sub rsp, 280
	mov rax, qword [rbp+24]
	cmp rax, 0
	je $n_1
	mov rax, 0
	jmp $n_2
$n_1:
	mov rax, 1
$n_2:
	mov rbx, rax
	cmp rbx, 0
	je if3_$n_4
	jmp if1_$n_2
if1_$n_2:
	mov rax, 1
	mov rsp, rbp
	pop rbp
	ret
	jmp if3_$n_3
if3_$n_4:
	mov rax, qword [rbp+24]
	sub rax, 1
	mov rbx , [rbp+16]
	mov [rbp-64], rax
	push qword [rbp-64]
	push rbx
	call fact$Main$int
	add rsp, 16
	mov rbx, qword [rbp+24]
	imul rbx, rax
	mov [rbp-72], rax
	mov rax, rbx
	mov rsp, rbp
	pop rbp
	ret
if3_$n_3:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
fact$Main$int$int$int:
	push rbp
	mov rbp, rsp
	sub rsp, 280
	mov rax, qword [rbp+24]
	cmp rax, qword [rbp+32]
	je $n_3
	mov rax, 0
	jmp $n_4
$n_3:
	mov rax, 1
$n_4:
	mov rbx, rax
	cmp rbx, 0
	je if3_$n_9
	jmp if1_$n_7
if1_$n_7:
	mov rax, qword [rbp+32]
	imul rax, qword [rbp+40]
	mov rsp, rbp
	pop rbp
	ret
	jmp if3_$n_8
if3_$n_9:
	mov rax, qword [rbp+24]
	sub rax, 1
	mov rbx , [rbp+16]
	mov [rbp-112], rax
	push qword [rbp+40]
	push qword [rbp+32]
	push qword [rbp-112]
	push rbx
	call fact$Main$int$int$int
	add rsp, 32
	mov rbx, qword [rbp+24]
	imul rbx, rax
	mov [rbp-120], rax
	mov rax, rbx
	mov rsp, rbp
	pop rbp
	ret
if3_$n_8:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
Main$Main:
	push rbp
	mov rbp, rsp
	sub rsp, 280
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
	sub rsp, 280
	mov rax,0
	push rax
	call malloc
	mov [rbp -144 ], rax
	add rsp, 8
	mov rsp, rbp
	pop rbp
	push rax
	call Imports$Imports
	add rsp, 8
	mov rbx, 5
	mov rcx, 6
	mov rdx, 7
	mov rsi, 5
	mov rbx , [rbp+16]
	mov [rbp-160], rcx
	mov [rbp-168], rdx
	mov [rbp-152], rsi
	push 10
	push 3
	push 5
	push rbx
	call fact$Main$int$int$int
	add rsp, 32
	mov rbx, qword [rbp-144]
	mov [rbp-176], rax
	mov [rbp-144], rbx
	push qword [rbp-176]
	push rbx
	call print$Imports$int
	add rsp, 16
	mov rbx, qword [rbp-144]
	mov [rbp-144], rbx
	push rbx
	call scan_int$Imports
	add rsp, 8
	mov rbx, qword [rbp-144]
	mov [rbp-200], rax
	mov [rbp-144], rbx
	push qword [rbp-200]
	push rbx
	call print$Imports$int
	add rsp, 16
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
