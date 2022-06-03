# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:56:35 2019

@author: Administrator
"""

import pickle
import os
import sys


# file1 = open('./contain_1000.txt','r')
# #file1 = open('./contain_500.txt','r')
# label_list = file1.read().split('\n')
# new_filenames1 = []
# #vul_lines = []
# for label in label_list:
#     filename = label.split('/')
#     file_name_label = filename[6]+filename[7]+filename[8]+'/'+filename[9]   #处理1000的
#     #file_name_label = filename[5]+filename[6]+filename[7]+'/'+filename[8]    #处理500的
#     casename = file_name_label.split(' ')[0]
#     new_filenames1.append(casename)
#     #vulline = file_name.split(' ')[1]

res = dict()

def main(folder_path, save_path):
    # f = open(pkl, 'rb')
    # names_vul_dict = pickle.load(f)
    # f.close()
    # new_filenames1 = []
    # for xname in names_vul_dict.keys():
    #     # new_filenames1.append(''.join(xname.split('/')[-4:-1])+ '/' + xname.split('/')[-1])
    #     new_filenames1.append('/'.join(xname.split('/')[-4:]))

    file2 = open(os.path.join(save_path, 'nvd_encodeliterals_string.txt'), 'a+')
    # new_label = []
    new_filenames = []

    confusion_change = []
    # folder_casename = []
    # new_filepath = './testcases_1000_new/'
    strings_2 = 'test_insert('
    strings_3 = ');'
    for software in os.listdir(folder_path):
        for software_version in os.listdir(os.path.join(folder_path, software)):
            for cve_id in os.listdir(os.path.join(folder_path, software, software_version)):
                for _dir in os.listdir(os.path.join(folder_path, software, software_version, cve_id)):
                    for case_file in os.listdir(os.path.join(folder_path, software, software_version, cve_id, _dir)):
                        if case_file.endswith('.c'):
                            filepath = os.path.join(folder_path, software, software_version, cve_id, _dir, case_file)
                            f = open(filepath, 'r')
                            sentences = f.read().split('\n')
                            f.close()

                            if len(sentences) > 2:
                                new_vullines = []
                                line_num = -1
                                insert_num = 0  # count test_insert tags
                                insert_lines = []
                                strings_indexs = []
                                strings_index_num = -1  # index tags

                                # index test_inset tag
                                i = 0
                                flag = True
                                while i < len(sentences):
                                    if strings_2 in sentences[i]:
                                        if 'void' not in sentences[i]:
                                            if strings_3 in sentences[i]:
                                                strings_index = 1
                                                strings_indexs.append(strings_index)
                                                i = i + 1
                                            else:
                                                if flag:
                                                    strings_index = 0
                                                    strings_indexs.append(strings_index)
                                                    strings_index = 1
                                                    strings_indexs.append(strings_index)
                                                    i = i + 2
                                                    flag = False
                                                else:
                                                    strings_index = 1
                                                    strings_indexs.append(strings_index)
                                                    strings_index = 0
                                                    strings_indexs.append(strings_index)
                                                    i = i + 2
                                                    flag = True
                                        else:
                                            strings_index = 0
                                            strings_indexs.append(strings_index)
                                            i = i + 1
                                    else:
                                        strings_index = 0
                                        strings_indexs.append(strings_index)
                                        i = i + 1

                                # print strings_indexs
                                if 1 in strings_indexs:
                                    if (strings_indexs.count(1) % 2) == 0:
                                        for strings_index in strings_indexs:
                                            strings_index_num = strings_index_num + 1
                                            if strings_index == 1:
                                                insert_num = insert_num + 1
                                                insert_lines.append(
                                                    strings_index_num)  # 得到插入的所有test_insert();行在sentences列表中的位置

                                        # for insert_line in insert_lines:
                                        for i in range(0, insert_num, 2):
                                            range_new_vul = int(insert_lines[i + 1]) - int(insert_lines[i])
                                            for j in range(1, range_new_vul):
                                                new_vulline = int(insert_lines[i] + 1) + j
                                                new_vullines.append(new_vulline)

                                        for new_vulline in new_vullines[:]:
                                            temp = sentences[new_vulline - 1].strip()
                                            if temp == '}' or temp == '' or temp == '{':
                                                new_vullines.remove(new_vulline)

                                        for new_vulline in new_vullines:
                                            new_filename = os.path.join(folder_path, software, software_version, cve_id, _dir,
                                                                        case_file + ' ' + str(new_vulline))
                                            # new_filename = '/home/sx/zigzag/zigzag-tang/deform-slice/sard-data-600-encode/'+testcase_1 + '/' + case_file+' '+str(new_vulline)
                                            new_filenames.append(new_filename)
                                    else:
                                        # num of test_insert tags is odd.[Not Handle]
                                        new_filename = os.path.join(folder_path, software, software_version, cve_id, _dir,
                                                                    case_file)
                                        # new_filename = '/home/sx/zigzag/zigzag-tang/deform-slice/sard-data-600-encode/'+testcase_1 + '/' + case_file
                                        confusion_change.append(new_filename)

                                else:
                                    # No test_insert tag means no flaw.
                                    insert_num = 0
                                    line_num = 0
                                    new_vullines.append(line_num)
                                    # testcase_names.append(testcase_name)
                                    new_filename = os.path.join(os.path.join(folder_path, software, software_version,
                                                                             cve_id, _dir, case_file + ' ' + str(new_vullines[0])))
                                    # new_filename = '/home/sx/zigzag/zigzag-tang/deform-slice/sard-data-600-encode/'+testcase_1 + '/' + case_file+' '+str(new_vullines[0])
                                    new_filenames.append(new_filename)
    count = 0
    for new_file in new_filenames:
        new_casename = new_file.split(' ')[0]
        new_casename_vulline = new_file.split(' ')[1]
        # if '/'.join(new_casename.split('/')[-4:]) in new_filenames1:
        if new_casename not in res.keys():
            count = count + 1
            res[new_casename] = set()
        res[new_casename].add(new_casename_vulline)
        file2.write(str(new_file) + '\n')
    file2.close()
    return count


if __name__ == '__main__':
    deform_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/deform-dataset-v3.1"
    save_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/deform-dataset-label-v3.1"

    for each in os.listdir(deform_path):
        result = main(os.path.join(deform_path, each), save_path)
        print os.path.join(deform_path, each) + "  " + str(result)

    with open(os.path.join(save_path, "DeformCaseName2VulLine.pkl"), "wb") as f:
        pickle.dump(res, f)
