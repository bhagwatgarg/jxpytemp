math_lib="""abs$Math$int:
	push rbp
	mov rbp, rsp
	sub rsp, 504
	mov rax, qword [rbp+24]
	cmp rax, 0
	jl $nn___1
	mov rax, 0
	jmp $nn___2
$nn___1:
	mov rax, 1
$nn___2:
	cmp rax, 0
	je if1_$nn___3
	jmp if1_$nn___2
if1_$nn___2:
	mov rax, qword [rbp+24]
	imul rax, -1
	mov qword [rbp+24], rax
if1_$nn___3:
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
	jl $nn___3
	mov rbx, 0
	jmp $nn___4
$nn___3:
	mov rbx, 1
$nn___4:
	mov qword [rbp-64], rax
	cmp rbx, 0
	je if1_$nn___6
	jmp if1_$nn___5
if1_$nn___5:
	mov qword rax, -1
	mov qword [rbp-64], rax
if1_$nn___6:
	mov rax, qword [rbp+24]
	cmp rax, 0
	jg $nn___5
	mov rax, 0
	jmp $nn___6
$nn___5:
	mov rax, 1
$nn___6:
	cmp rax, 0
	je if1_$nn___9
	jmp if1_$nn___8
if1_$nn___8:
	mov qword rax, 1
	mov qword [rbp-64], rax
if1_$nn___9:
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
	jg $nn___7
	mov rax, 0
	jmp $nn___8
$nn___7:
	mov rax, 1
$nn___8:
	cmp rax, 0
	je if1_$nn___12
	jmp if1_$nn___11
if1_$nn___11:
	mov rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
if1_$nn___12:
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
	jl $nn___9
	mov rax, 0
	jmp $nn___10
$nn___9:
	mov rax, 1
$nn___10:
	cmp rax, 0
	je if1_$nn___15
	jmp if1_$nn___14
if1_$nn___14:
	mov rax, qword [rbp+24]
	mov rsp, rbp
	pop rbp
	ret
if1_$nn___15:
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
	jl $nn___11
	mov rax, 0
	jmp $nn___12
$nn___11:
	mov rax, 1
$nn___12:
	cmp rax, 0
	je if1_$nn___18
	jmp if1_$nn___17
if1_$nn___17:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
if1_$nn___18:
	mov qword rax, 2
	mov qword [rbp-192], rax
for_$nn___20:
	mov rax, qword [rbp-192]
	imul rax, qword [rbp-192]
	cmp rax, qword [rbp+24]
	jle $nn___13
	mov rax, 0
	jmp $nn___14
$nn___13:
	mov rax, 1
$nn___14:
	cmp rax, 0
	je for_$nn___26
	jmp for_$nn___22
for_$nn___21:
	mov qword rax, qword [rbp-192]
	mov rbx, rax
	add rbx, 1
	mov qword [rbp-192], rax
	mov qword [rbp-192], rbx
	jmp for_$nn___20
for_$nn___22:
	mov rax, qword [rbp+24]
	cdq
	idiv qword [rbp-192]
	mov rax, rdx
	cmp rax, 0
	je $nn___15
	mov rax, 0
	jmp $nn___16
$nn___15:
	mov rax, 1
$nn___16:
	mov qword [rbp-232], rdx
	cmp rax, 0
	je if1_$nn___25
	jmp if1_$nn___24
if1_$nn___24:
	mov rax, 0
	mov rsp, rbp
	pop rbp
	ret
if1_$nn___25:
	jmp for_$nn___21
for_$nn___26:
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
\tsub rsp, 16
\tmov rsi, rsp
\tmov rdi, sint
\txor rax, rax
\tcall scanf
\tmov rax, qword [rsp]
\t add rsp, 16
\tmov rsp, rbp
\tpop rbp
\tret"""