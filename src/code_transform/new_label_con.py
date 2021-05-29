# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:56:35 2019

@author: Administrator
"""

import pickle
import os

file1 = open('./contain_1000.txt','r')
#file1 = open('./contain_500.txt','r')
label_list = file1.read().split('\n')
new_filenames1 = []
#vul_lines = []
for label in label_list:
    filename = label.split('/')
    file_name_label = filename[6]+filename[7]+filename[8]+'/'+filename[9]   
    #file_name_label = filename[5]+filename[6]+filename[7]+'/'+filename[8]    
    casename = file_name_label.split(' ')[0]
    new_filenames1.append(casename)
    #vulline = file_name.split(' ')[1]


folder_path = './encodeliterals_string_1000_test/'
file2 = open('./contain_encodeliterals_string_1000.txt','a+')
#new_label = []
new_filenames = []

confusion_change = []
#folder_casename = []
#new_filepath = './testcases_1000_new/'
strings_2 = 'test_insert('
for testcase_1 in os.listdir(folder_path):
    for testcase_2 in os.listdir(os.path.join(folder_path,testcase_1)):
        for testcase_3 in os.listdir(os.path.join(folder_path,testcase_1,testcase_2)):
            for case_file in os.listdir(os.path.join(folder_path,testcase_1,testcase_2,testcase_3)):
                if case_file.endswith('.c'):
                    filepath = os.path.join(folder_path,testcase_1,testcase_2,testcase_3,case_file)
                    f=open(filepath,'r')
                    sentences = f.read().split('\n')
                    f.close()
                    
                    if len(sentences) > 2:
                        new_vullines = []
                        line_num = -1
                        insert_num = 0
                        insert_lines = []
                        strings_indexs = []
                        strings_index_num = -1
                    
                        for sentence in sentences:
                            if strings_2 in sentence:
                                if 'void' not in sentence:
                                    strings_index = 1
                                    strings_indexs.append(strings_index)
                                
                            else:
                                strings_index = 0
                                strings_indexs.append(strings_index)
                        
                        if 1 in strings_indexs:
                            if (strings_indexs.count(1) % 2) == 0:
                                for strings_index in strings_indexs:
                                    strings_index_num = strings_index_num + 1
                                    if strings_index == 1:
                                        insert_num = insert_num + 1
                                        insert_lines.append(strings_index_num)                            
                                #for insert_line in insert_lines:
                                for i in range(0,insert_num,2):
                                    range_new_vul = int(insert_lines[i+1]) - int(insert_lines[i])
                                    for j in range(1,range_new_vul):
                                        new_vulline = int(insert_lines[i]+1) + j
                                        new_vullines.append(new_vulline)
                                    
                                for new_vulline in new_vullines:
                                    for k in range(0,10):
                                        strings_1 = ' ' * k +'}'
                                        #print(strings_1)
                                        if sentences[new_vulline-1] == strings_1:
                                            new_vullines.remove(new_vulline)
                                        else:
                                            continue
                                
                                    for j in range(0,20):
                                        strings_1 = ' ' * j
                                        #print(strings_1)
                                        if sentences[new_vulline-1] == strings_1:
                                            new_vullines.remove(new_vulline)
                                            #print(strings_1)
                                        else:
                                            continue
                                    
                                    
                                for new_vulline in new_vullines:
                                    new_filename = '/home/ldx/2019/slicerget/confusion_encodeliterals_string_test/'+testcase_1 + '/' + testcase_2 + '/' + testcase_3 +'/' + case_file+' '+str(new_vulline)
                                    new_filenames.append(new_filename)
                            else:
                                new_filename = '/home/ldx/2019/slicerget/confusion_encodeliterals_string_test/'+testcase_1 + '/' + testcase_2 + '/' + testcase_3 +'/' + case_file
                                confusion_change.append(new_filename)
                                
                        else:
                            insert_num = 0
                            line_num = 0
                            new_vullines.append(line_num)
                            #testcase_names.append(testcase_name)
                            new_filename = '/home/ldx/2019/slicerget/confusion_encodeliterals_string_test/'+testcase_1 + '/' + testcase_2 + '/' + testcase_3 +'/' + case_file+' '+str(new_vullines[0])
                            new_filenames.append(new_filename)

for new_file in new_filenames:
    new_file_casename = new_file.split('/')
    new_file_name_label = new_file_casename[6]+new_file_casename[7]+new_file_casename[8]+'/'+new_file_casename[9]
    new_casename = new_file_name_label.split(' ')[0]
    if new_casename in new_filenames1:
        file2.write(str(new_file)+'\n')
file2.close()

                    