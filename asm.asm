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
	push ebp
	mov ebp, esp
	mov esi, dword [ebp+12]
	mov edi, pint
	push edi
	push esi
	xor eax, eax
	call printf
	add esp, 4
	xor eax, eax
	mov esp, ebp
	pop ebp
	ret
scan_int$Imports:
	push ebp
	mov ebp, esp
	push esi
	push edi
	add esp, 4
	mov esi, esp
	lea edi, [rel sint]
	xor eax, eax
	call scanf
	mov eax, dword [esp]
	pop edi
	pop esi
	mov esp, ebp
	pop ebp
	ret
        
Imports$Imports:
	push ebp
	mov ebp, esp
	sub esp, 88
	mov esp, ebp
	pop ebp
	ret
Main$Main:
	push ebp
	mov ebp, esp
	sub esp, 88
	mov esp, ebp
	pop ebp
	ret
main:
	mov eax,0 
	push ebp 
	mov ebp, esp 
	push eax 
	call malloc 
	add esp, 4 
	mov esp, ebp 
	push eax 
	call Main$Main 
	add esp, 4 
	push eax 
	call main$Main 
	add esp, 4 
	pop ebp 
	ret
main$Main:
	push ebp
	mov ebp, esp
	sub esp, 88
	mov eax,0
	push eax
	call malloc
	mov [ebp -20 ], eax
	add esp, 4
	mov esp, ebp
	pop ebp
	push eax
	call Imports$Imports
	add esp, 4
	mov  ebx, 0
	mov  ecx, 0
	mov dword [ebp-20], eax
	mov dword [ebp-24], ecx
for_$n_2:
	mov eax, dword [ebp-24]
	cmp eax, 10
	jl $n_1
	mov eax, 0
	jmp $n_2
$n_1:
	mov eax, 1
$n_2:
	mov ebx, eax
	cmp ebx, 0
	je for_$n_5
	jmp for_$n_4
for_$n_3:
	mov eax, dword [ebp-24]
	add eax, 1
	mov dword [ebp-24], eax
	jmp for_$n_2
for_$n_4:
	mov  eax, dword [ebp-20]
	mov dword [ebp-20], eax
	push dword [ebp-24]
	push eax
	call print$Imports$int
	add esp, 8
	jmp for_$n_3
for_$n_5:
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
