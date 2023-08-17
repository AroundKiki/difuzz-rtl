'''
Author: Xutong
Date: 2023-07-05 03:47:55
FilePath: /difuzz-rtl/inst_generate/asm_generate.py
Description: 使用difuzz-rtl的代码随机生成命令并编译
'''
# import os
# os.environ['PYTHONPATH']="/root/workDir/difuzz-rtl/Fuzzer1:/root/workDir/difuzz-rtl:/root/workDir/difuzz-rtl/Fuzzer1/RTLSim/src"
import sys
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1")
sys.path.append("/root/workDir/difuzz-rtl")
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1/RTLSim/src")
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1/src")
sys.path.append("/root/elf2hex/elf2hex-1.0.1")



from Fuzzer1.src.preprocessor import rvPreProcessor
from Fuzzer1.src.mutator import simInput, rvMutator
import random




cc = 'riscv64-unknown-elf-gcc'
# elf2hex = 'riscv64-unknown-elf-elf2hex'
elf2hex = "elf2hex"
template = 'Fuzzer1/Template'   #路径 
out = 'output'      #路径
proc_num =  "test"       #用于区分不同进程
no_guide = False

mutator = rvMutator(no_guide=no_guide)

preprocessor = rvPreProcessor(cc, elf2hex, template, out, proc_num)

prob_intr = 0
assert_intr = False
if random.random() < prob_intr:
    assert_intr = True


(sim_input, data) = mutator.get(assert_intr)

preprocessor.process(sim_input, data, assert_intr)