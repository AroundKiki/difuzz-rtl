'''
Author: Xutong
Date: 2023-05-31 02:45:35
FilePath: /difuzz-rtl/inst_generate/main.py
Description: 随机生成初始数据集
'''
import sys
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1")
sys.path.append("/root/workDir/difuzz-rtl")
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1/RTLSim/src")
sys.path.append("/root/workDir/difuzz-rtl/Fuzzer1/src")
sys.path.append("/root/elf2hex/elf2hex-1.0.1")
from Fuzzer1.src.mutator import simInput, rvMutator
import random 
from multiprocessing import Pool

no_guide = True # Only random testing?
prob_intr = 0 # Probability of asserting interrupt
debug = True

assert_intr = False
if random.random() < prob_intr:
    assert_intr = True


with open("test_command_10000_20.txt", "w") as f:

    mutator = rvMutator(no_guide=no_guide)
    inst_sets = []


    for i in range(10000):
        (sim_input, data) = mutator.get(assert_intr)

        inst_set = []
        if debug:
            # print('[DifuzzRTL] Fuzz Instructions')
            # for inst, INT in zip(sim_input.get_insts(), sim_input.ints + [0]):
            #     print('{:<50}{:04b}'.format(inst, INT))
            inst_set.append('<cls>')
            f.write("<cls>\n")
            for inst in sim_input.get_insts():
                # print(inst)
                inst = inst.replace(",", " ,")
                inst = inst.replace(":", " :")

                inst_set.append(inst)
                f.write(inst + '<sep>' + '\n')
            # f.write("\n")
        inst_sets.append(inst_set)
        

