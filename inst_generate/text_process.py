'''
Author: Xutong
Date: 2023-07-11 03:50:03
FilePath: /diffusion-lm/text_process.py
Description: 
    删除生成内容里的<cls> 和<sep>，并让指令之间换行
    不同的数据之间用空行分开
    输出edited_output.txt
'''
import os

filepath = "output/2.txt"

with open(filepath, "r+") as f:
    text = f.readlines()
    for i in range(len(text)):
        text[i] = text[i].replace("<cls> ", "\n")
        text[i] = text[i].replace("<sep> ", "\n")   #带空格
        text[i] = text[i].replace("<sep>", "")    #不带空格
    
with open(filepath.split(".")[0]+"edited.txt", "w+") as f:
    for line in text:
        f.write(line)
        f.write("\n")
        



