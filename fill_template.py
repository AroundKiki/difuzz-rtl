# 组合生成.S文件

templates = [ 'p-m', 'p-s', 'p-u',
              'v-u']
version = 0
test_template = "Fuzzer1/Template" + '/rv64-{}.S'.format(templates[version])
# test_template = "Fuzzer1/Template" + '/rv64-{}.S'.format(templates[version])


fd = open(test_template, 'r')
template_lines = fd.readlines()
fd.close()


sample_num = 8
for i in range(sample_num):
    assembly = []
    for line in template_lines:
        assembly.append(line)
        # if '_fuzz_prefix:' in line:
        #     for inst in prefix_insts:
        #         assembly.append(inst + ';\n')

        if '_fuzz_main:' in line:
            for inst in insts:
                assembly.append(inst + ';\n')

        # if '_fuzz_suffix:' in line:
        #     for inst in suffix_insts:
        #         assembly.append(inst + ';\n')

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

    fd = open(asm_name, 'w')
    fd.writelines(assembly)
    fd.close()