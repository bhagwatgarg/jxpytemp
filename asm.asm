['func', 'main$Main', '[]', '']
['_temp1', '1', '2', 'int_+']
['a$main$Main', '_temp1', '', 'int_=']
['b$main$Main', '3.0', '', 'float_=']
['_temp3', 'a$main$Main', '', 'int_float_=']
['_temp2', '_temp3', 'b$main$Main', 'float_+']
['_temp2', 'c$main$Main', '_temp2', 'float_=']
['ret', 'c$main$Main', '', '']
[0, 8]
8
extern malloc

section	.data

_temp1	dd	0
_temp3	dd	0
_temp2	dd	0

section .text
	global main
	mov rax, 1
	add rax, 2
	movsd xmm0, qword3.0
	cvtsi2ss xmm1, qworda$main$Main
	mov xmm2, xmm1
	addsd xmm2, xmm0
	mov _temp1, rax
	movsd b$main$Main, xmm0
	movsd _temp3, xmm1
	movsd _temp2, xmm2
	mov rax, qwordc$main$Main
	mov rsp, rbp
	pop rbp
	ret
