.global _start
.data
results: .space 8 * 256
calc_stack: .space 8 * 256
stack_top: .word 0
mem_C: .double 0.0
.text
_start:
    ldr r10, =calc_stack
    ldr r11, =stack_top
    @ Linha 1
    ldr r0, =0x41400000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40800000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    sub r1, r1, #8
    add r3, r10, r1
    vldr d1, [r3]
    vdiv.f64 d0, d1, d0
    vstr d0, [r3]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 3.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #0
    vstr d0, [r0]
    @ Linha 2
    ldr r0, =0x40400000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40400000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    sub r1, r1, #8
    add r3, r10, r1
    vldr d1, [r3]
    vmul.f64 d0, d1, d0
    vstr d0, [r3]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 9.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #8
    vstr d0, [r0]
    @ Linha 3
    ldr r0, =0x41000000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40000000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    @ operador // tratado na infraestrutura Python
    @ resultado previsto: 4.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #16
    vstr d0, [r0]
    @ Linha 4
    ldr r0, =0x41880000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40a00000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    @ operador % tratado na infraestrutura Python
    @ resultado previsto: 2.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #24
    vstr d0, [r0]
    @ Linha 5
    ldr r0, =0x40000000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40a00000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    @ operador ^ tratado na infraestrutura Python
    @ resultado previsto: 32.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #32
    vstr d0, [r0]
    @ Linha 6
    ldr r0, =0x41a40000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =mem_C
    vldr d0, [r0]
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 20.5
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #40
    vstr d0, [r0]
    @ Linha 7
    ldr r0, =mem_C
    vldr d0, [r0]
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x3fc00000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    sub r1, r1, #8
    add r3, r10, r1
    vldr d1, [r3]
    vadd.f64 d0, d1, d0
    vstr d0, [r3]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 22.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #48
    vstr d0, [r0]
    @ Linha 8
    ldr r0, =0x3f800000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 22.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #56
    vstr d0, [r0]
    @ Linha 9
    ldr r0, =0x40000000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40400000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    sub r1, r1, #8
    add r3, r10, r1
    vldr d1, [r3]
    vadd.f64 d0, d1, d0
    vstr d0, [r3]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 25.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #64
    vstr d0, [r0]
    @ Linha 10
    ldr r0, =0x41100000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x3f800000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    sub r1, r1, #8
    add r3, r10, r1
    vldr d1, [r3]
    vsub.f64 d0, d1, d0
    vstr d0, [r3]
    add r1, r1, #8
    str r1, [r11]
    ldr r0, =0x40000000
    vmov s0, r0
    vcvt.f64.f32 d0, s0
    ldr r1, [r11]
    add r2, r10, r1
    vstr d0, [r2]
    add r1, r1, #8
    str r1, [r11]
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    sub r1, r1, #8
    add r3, r10, r1
    vldr d1, [r3]
    vdiv.f64 d0, d1, d0
    vstr d0, [r3]
    add r1, r1, #8
    str r1, [r11]
    @ resultado previsto: 4.0
    ldr r1, [r11]
    sub r1, r1, #8
    add r2, r10, r1
    vldr d0, [r2]
    ldr r0, =results
    add r0, r0, #72
    vstr d0, [r0]
_halt:
    b _halt
