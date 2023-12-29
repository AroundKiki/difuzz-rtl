#已被makefile的编译替代

import subprocess

cc = 'riscv64-unknown-elf-gcc'
# elf2hex = 'riscv64-unknown-elf-elf2hex'
elf2hex = "elf2hex"
template = 'Fuzzer1/Template'   #路径 
out = 'output'      #路径
proc_num =  "test"       #用于区分不同进程
no_guide = False


cc_args = [ cc, '-march=rv64g', '-mabi=lp64', '-static', '-mcmodel=medany',
                         '-fvisibility=hidden', '-nostdlib', '-nostartfiles',
                         '-I', '{}/include'.format(template),
                         '-I', '/usr/include',
                         '-T', '{}/include/link.ld'.format(template) ]

elf2hex_args = [ elf2hex, '--bit-width', '64', '--input' ]

intr = False

if intr: DINTR = ['-DINTERRUPT']
else: DINTR = []
extra_args = DINTR + [ '-I', '{}/include/p'.format(template) ]

base = "output_source"
si_name = base + '/.input_{}.si'.format(proc_num)
asm_name = base + '/.input_{}.S'.format(proc_num)
elf_name = base + '/.input_{}.elf'.format(proc_num)
hex_name = base + '/.input_{}.hex'.format(proc_num)
sym_name = base + '/.input_{}.symbols'.format(proc_num)
rtl_intr_name = base + '/.input_{}.rtl.intr'.format(proc_num)
isa_intr_name = base + '/.input_{}.isa.intr'.format(proc_num)

asm_name = "output_source/source1.S"

cc_args = cc_args + extra_args + [ asm_name, '-o', elf_name ]
cc_ret = -1
while True:
    cc_ret = subprocess.call(cc_args)
    # if cc_ret == -9: cc process is killed by OS due to memory usage
    if cc_ret != -9: break

if cc_ret == 0:
    subprocess.call(cc_args)

    elf2hex_args = elf2hex_args + [ elf_name, '--output', hex_name]
    subprocess.call(elf2hex_args)
