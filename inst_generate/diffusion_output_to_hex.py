'''
Author: Xutong
Date: 2023-07-18 17:14:32
FilePath: /difuzz-rtl/inst_generate/diffusion_output_to_hex.py
Description: 
'''
'''
Author: Xutong
Date: 2023-07-18 16:17:51
FilePath: /difuzz-rtl/inst_generate/diffusion_output_to_hex.py
Description: 组合多个脚本，从diffusion model的原始输出生成hex

'''

import os
import sys
import subprocess


sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1")
sys.path.append("/root/workDir/difuzz-rtl")
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1/RTLSim/src")
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1/src")
sys.path.append("/root/elf2hex/elf2hex-1.0.1")

from src.mutator import simInput, rvMutator


#===============参数区=================
filepath = "model_output/1.txt"

templates = [ 'p-m', 'p-s', 'p-u',
              'v-u']
version = 0
test_template = "Fuzzer1/Template" + '/rv64-{}.S'.format(templates[version])

no_guide = False
mutator = rvMutator(no_guide=no_guide)
assert_intr = False

num_data_sections = 6



#======================================


def format_output(filepath):
    # 去掉<cls>,<sep>符号
    with open(filepath, "r+") as f:
        text = f.readlines()
        for i in range(len(text)):
            text[i] = text[i].replace("<cls> ", "")
            text[i] = text[i].replace("<sep> ", "\n")   #带空格
            text[i] = text[i].replace("<sep>", "")    #不带空格
        
    with open(filepath.split(".")[0]+"edited.txt", "w+") as f:
        for line in text:
            f.write(line)
            f.write("\n")
    
    with open(filepath.split(".")[0]+"edited.txt", "r") as f:
        return f.readlines()        #读取后字符串内部的\n会断开
    
def group_command(lines):
    # 将命令分组存放
    dataset = []
    data = []
    for line in lines:
        if not line.isspace():
            data.append(line)
        else:
            dataset.append(data)
            data = []
    
    return dataset

def generate_source(lines):
    fd = open(test_template, 'r')
    template_lines = fd.readlines()
    fd.close()

    (sim_input, data) = mutator.get(assert_intr)

    prefix_insts = sim_input.get_prefix()
    # insts = sim_input.get_insts()
    suffix_insts = sim_input.get_suffix()
    sim_input_ints = sim_input.ints.copy()


    section_size = len(data) // num_data_sections


    assembly = []
    for line in template_lines:
        assembly.append(line)
        if '_fuzz_prefix:' in line:
            for inst in prefix_insts:
                assembly.append(inst + ';\n')

        if '_fuzz_main:' in line:
            # 模型生成的代码
            for inst in lines:
                assembly.append(inst)

        if '_fuzz_suffix:' in line:
            for inst in suffix_insts:
                assembly.append(inst + ';\n')

        for n in range(num_data_sections):
            start = n * section_size
            end = start + section_size
            if '_random_data{}'.format(n) in line:
                k = 0
                for i in range(start, end, 2):
                    label = ''
                    if i > start + 2 and i < end - 4:
                        label = 'd_{}_{}:'.format(n, k)
                        k += 1

                    assembly.append('{:<16}.dword 0x{:016x}, 0x{:016x}\n'.\
                                    format(label, data[i], data[i+1]))
                    
    return assembly

def s_to_hex(source_path):
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

    asm_name = source_path
    elf_name = source_path.split(".")[0] + ".elf"
    hex_name = source_path.split(".")[0] + ".hex"

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

if __name__=="__main__":
    # 返回值中
    formatted_lines = format_output(filepath)
    dataset = group_command(formatted_lines)
    for i,data in enumerate(dataset):
        assembly = generate_source(data)
        fd = open("output_source/source"+str(i)+".S", 'w')
        fd.writelines(assembly)
        fd.close()
        s_to_hex("output_source/source"+str(i)+".S")
    
    pass

    


