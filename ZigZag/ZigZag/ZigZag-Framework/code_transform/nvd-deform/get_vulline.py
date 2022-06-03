#-*- coding:utf-8 -*-

from __future__ import print_function
import os
import pickle


log_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/log-get-vulline.txt"
log = open(log_path, "w")
code_path = '/home/ZigZag/Dataset/real-world-programs'
diff_path = '/home/ZigZag/Dataset/diffs'
vulline_dict = {}
patchline_dict = {}
_dict_vul_code = {} 
_dict_patch_code = {} 
for folder_1 in os.listdir(code_path):
    for folder_2 in os.listdir(os.path.join(code_path,folder_1)):
        for folder_3 in os.listdir(os.path.join(code_path,folder_1,folder_2)):
            for folder_4 in os.listdir(os.path.join(code_path,folder_1,folder_2,folder_3)):
                for filename in os.listdir(os.path.join(code_path,folder_1,folder_2,folder_3,folder_4)):
                    filepath = os.path.join(code_path,folder_1,folder_2,folder_3,folder_4,filename)

                    diff = os.path.join(diff_path,folder_1,folder_2,folder_3,folder_4+".diff")
                    if not os.path.exists(diff):
                        print(">>> Error: " + diff, file=log)
                    with open(diff, "r") as f:
                        sens = f.read().split('\n')
                    print(">>> File Path: " + filepath, file=log)
                    print(">>> diff Path: " + diff, file=log)
                    # difffolder = os.path.join(diff_path,folder_1,folder_2,folder_3)
                    # for filename2 in os.listdir(difffolder):
                    #     diffpath = os.path.join(difffolder,filename2)
                    #     f2 = open(diffpath,'r')
                    #     sens = f2.read().split('\n')
                    #     f2.close()
                    #print(diffpath)
                    if filepath not in _dict_vul_code.keys():
                        _dict_vul_code[filepath] = {}
                    if filepath not in _dict_patch_code.keys():
                        _dict_patch_code[filepath] = {}

                    index = -1
                    index_start = []
                    for sen in sens:
                        #print(sen)
                        index += 1
                        if sen.startswith('@@ ') is True: 
                            index_start.append(index)
                    for i in range(0,len(index_start)):
                        if i < len(index_start)-1:
                            diff_sens = sens[index_start[i]:index_start[i+1]] 
                        else:
                            diff_sens = sens[index_start[i]:]
                        startline = diff_sens[0]
                        vul_linenum = int(startline.split('-')[1].split(',')[0]) 
                        patch_linenum = int(startline.split('+')[1].split(',')[0]) 
                        diff_sens = diff_sens[1:] 
                        index = -1
                        for sen in diff_sens:
                            if sen.startswith('-') is True and sen.startswith('---') is False:
                                index += 1
                                linenum = index + vul_linenum
                                _dict_vul_code[filepath][linenum] = sen.strip('-').strip()
                            elif sen.startswith('+') is True and sen.startswith('+++') is False:
                                linenum = index + patch_linenum
                                _dict_patch_code[filepath][linenum] = sen.strip('+').strip()
                            else:
                                index += 1

                    #print(_dict_vul_code)
                
                    with open(filepath, 'r') as f1:
                        sentences = f1.read().split('\n')
                    if filepath.find('OLD') != -1:
                        if filepath in _dict_vul_code.keys():
                            print(filepath)
                            for line in _dict_vul_code[filepath].keys():
                                print(line)
                                if line > len(sentences):
                                    continue
                                vul_sen = sentences[line-1].strip()
                                if vul_sen != _dict_vul_code[filepath][line] : 
                                    continue
                                else:
                                    if filepath not in vulline_dict.keys():
                                        vulline_dict[filepath] = [line]
                                    else:
                                        vulline_dict[filepath].append(line)

                    # elif filepath.find('NEW') != -1:
                    #     if filepath in _dict_patch_code.keys():
                    #         for line in _dict_patch_code[filepath].keys():
                    #             patch_sen = sentences[line-1].strip()
                    #             if patch_sen != _dict_patch_code[filepath][line] :
                    #                 continue
                    #             else:
                    #                 if filepath not in patchline_dict.keys():
                    #                     patchline_dict[filepath] = [line]
                    #                 else:
                    #                     patchline_dict[filepath].append(line)
                    # else:
                    #     print(">>> File Error!", file=log)
print(vulline_dict, file=log)
with open('./vul_lines.pkl','wb') as f:
    pickle.dump(vulline_dict,f)
log.close()