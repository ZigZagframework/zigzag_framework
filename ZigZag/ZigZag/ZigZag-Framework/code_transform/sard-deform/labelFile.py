# -*- coding: utf-8 -*-

import pickle
import os
import sys

if __name__ == "__main__":
    f = open(sys.argv[1], 'rb')
    names_vul_dict = pickle.load(f)
    f.close()

    folder_path = sys.argv[2]
    save_path = sys.argv[3]

    #folder_path = '/home/sx/zigzag/zigzag-tang/deform-slice/sard-data-600-insert/'
    #folder_casename = []
    strings_2 = '/*Insert_confusion_labels_2021_12*/'
    strings_3 = 'void test_insert(void){}'
    count_vul = 0
    count_non_vul = 0
    count_err = 0
    for testcase_1 in os.listdir(folder_path):
        for testcase_2 in os.listdir(os.path.join(folder_path,testcase_1)):
            for testcase_3 in os.listdir(os.path.join(folder_path,testcase_1,testcase_2)):
                os.system("mkdir -p " + os.path.join(save_path,testcase_1,testcase_2,testcase_3))
                for case_file in os.listdir(os.path.join(folder_path,testcase_1,testcase_2,testcase_3)):
                    new_key = os.path.join(save_path,testcase_1,testcase_2,testcase_3,case_file)
                    old_key = os.path.join(folder_path,testcase_1,testcase_2,testcase_3,case_file)
                    print(old_key)
                    with open(old_key, "r") as f:
                        sentences = f.read().split('\n')
                    if old_key in names_vul_dict.keys():
                        count_vul = count_vul + 1
                        vullines = list(int(x) for x in names_vul_dict[old_key])
                        vullines.sort()
                        print(vullines)
                        if 0 not in vullines:
                            for j in range(len(vullines)):
                                vulline = vullines[j]
                                print(vulline)
                                vulline = vulline + 2 * j
                                tokens = sentences[vulline - 1].split(' ')
                                tab_num = 0
                                for token in tokens:
                                    if token == '':
                                        tab_num = tab_num + 1
                                strings_1 = ' ' * tab_num + 'test_insert();'
                                sentences.insert(vulline - 1,strings_1)
                                sentences.insert(vulline + 1,strings_1)
                            sentences.insert(-1,strings_3)
                            sentences.insert(-1,strings_2)
                        else:
                            count_err = count_err + 1
                    else:
                        count_non_vul = count_non_vul + 1
                    f1 = open(new_key,'w')
                    for sentence_new in sentences:
                        f1.write(sentence_new+'\n')
                    f1.close()
    print("Vul File: " + str(count_vul))
    print("Non-Vul File: " + str(count_non_vul))
    print("Err File: " + str(count_err))