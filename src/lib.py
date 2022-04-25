math_lib="""abs$Math$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	cmp rax, 0
	jl $n_1
	mov rax, 0
	jmp $n_2
$n_1:
	mov rax, 1
$n_2:
	cmp rax, 0
	je if1_$n_3
	jmp if1_$n_2
if1_$n_2:
	mov rax, qword [rbp+24]
	imul rax, -1
	mov qword [rbp+24], rax
if1_$n_3:
	mov rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
signum$Math$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov qword rax, 0
	mov rbx, qword [rbp+24]
	cmp rbx, 0
	jl $n_3
	mov rbx, 0
	jmp $n_4
$n_3:
	mov rbx, 1
$n_4:
	mov qword [rbp-64], rax
	cmp rbx, 0
	je if1_$n_6
	jmp if1_$n_5
if1_$n_5:
	mov qword rax, -1
	mov qword [rbp-64], rax
if1_$n_6:
	mov rax, qword [rbp+24]
	cmp rax, 0
	jg $n_5
	mov rax, 0
	jmp $n_6
$n_5:
	mov rax, 1
$n_6:
	cmp rax, 0
	je if1_$n_9
	jmp if1_$n_8
if1_$n_8:
	mov qword rax, 1
	mov qword [rbp-64], rax
if1_$n_9:
	mov rax, qword [rbp-64]
	mov rsp, rbp
	pop rbp
	ret
max$Math$int$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	cmp rax, qword [rbp+32]
	jg $n_7
	mov rax, 0
	jmp $n_8
$n_7:
	mov rax, 1
$n_8:
	cmp rax, 0
	je if1_$n_12
	jmp if1_$n_11
if1_$n_11:
	mov rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
if1_$n_12:
	mov rax, qword [rbp+32]
	mov rsp, rbp
	pop rbp
	ret
min$Math$int$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	cmp rax, qword [rbp+32]
	jl $n_9
	mov rax, 0
	jmp $n_10
$n_9:
	mov rax, 1
$n_10:
	cmp rax, 0
	je if1_$n_15
	jmp if1_$n_14
if1_$n_14:
	mov rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
if1_$n_15:
	mov rax, qword [rbp+32]
	mov rsp, rbp
	pop rbp
	ret
square$Math$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	imul rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
cube$Math$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	imul rax, qword [rbp+24]
	imul rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
is_prime$Math$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	cmp rax, 2
	jl $n_11
	mov rax, 0
	jmp $n_12
$n_11:
	mov rax, 1
$n_12:
	cmp rax, 0
	je if1_$n_18
	jmp if1_$n_17
if1_$n_17:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
if1_$n_18:
	mov qword rax, 2
	mov qword [rbp-192], rax
for_$n_20:
	mov rax, qword [rbp-192]
	imul rax, qword [rbp-192]
	cmp rax, qword [rbp+24]
	jle $n_13
	mov rax, 0
	jmp $n_14
$n_13:
	mov rax, 1
$n_14:
	cmp rax, 0
	je for_$n_26
	jmp for_$n_22
for_$n_21:
	mov qword rax, qword [rbp-192]
	mov rbx, rax
	add rbx, 1
	mov qword [rbp-192], rax
	mov qword [rbp-192], rbx
	jmp for_$n_20
for_$n_22:
	mov rax, qword [rbp+24]
	cdq
	idiv qword [rbp-192]
	mov rax, rdx
	cmp rax, 0
	je $n_15
	mov rax, 0
	jmp $n_16
$n_15:
	mov rax, 1
$n_16:
	mov qword [rbp-232], rdx
	cmp rax, 0
	je if1_$n_25
	jmp if1_$n_24
if1_$n_24:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
if1_$n_25:
	jmp for_$n_21
for_$n_26:
	mov rax, 1
	mov rsp, rbp
	pop rbp
	ret"""

print_int="""print$Imports$int:	
	push rbp
	mov rbp, rsp

	push rsi
	push rdi
	push rax
	push rbx
	push rcx
	push rdx
	mov rsi, qword [rbp+24]
	mov rdi, pint
	xor rax, rax

	call printf

	xor rax, rax
	pop rdx
	pop rcx
	pop rbx
	pop rax
	pop rdi
	pop rsi

	mov rsp, rbp
	pop rbp
	ret"""

scan_int="""scan_int$Imports:
\tpush rbp
\tmov rbp, rsp
\tpush rsi
\tpush rdi
\tadd rsp, 8
\tmov rsi, rsp
\tlea rdi, [rel sint]
\txor rax, rax
\tcall scanf
\tmov rax, qword [rsp]
\tpop rdi
\tpop rsi
\tmov rsp, rbp
\tpop rbp
\tret"""