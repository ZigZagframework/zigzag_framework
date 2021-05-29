# -*- coding: utf-8 -*-
"""
@author: Administrator
"""
import os

file1 = open('./contain_1000.txt','r')
label_list = file1.read().split('\n')
new_vullines = []
names_vul_dict = {}
#vul_lines = []
for label in label_list:
    filename = label.split('/')
    file_name_label = filename[6]+filename[7]+filename[8]+'/'+filename[9] 
    #file_name_label = filename[5]+filename[6]+filename[7]+'/'+filename[8]
    casename_file1 = file_name_label.split(' ')[0] #testcase+filename
    vulline_file1 = file_name_label.split(' ')[1] 
    if casename_file1 not in names_vul_dict.keys():
        names_vul_dict[casename_file1] = [vulline_file1]
    else:
        new_vullines = names_vul_dict[casename_file1]
        #print("new_vullines:")
        #print(new_vullines)
        for i in range(len(new_vullines)):
            if vulline_file1 not in new_vullines:
                if vulline_file1 < new_vullines[i]:
                    new_vullines.insert(i,vulline_file1)
                else:
                    continue
        if vulline_file1 > new_vullines[-1]:
            if vulline_file1 not in new_vullines:
                new_vullines.append(vulline_file1)
        names_vul_dict[casename_file1] = new_vullines
        #print(casename_file1)
    #vulline = file_name.split(' ')[1]
    #vul_lines.append(vulline)

folder_path = './testcases_1000/'
#folder_casename = []
strings_2 = '/*Insert_confusion_labels_2019_04*/'
strings_3 = 'void test_insert(void){}'
for testcase_1 in os.listdir(folder_path):
    for testcase_2 in os.listdir(os.path.join(folder_path,testcase_1)):
        for testcase_3 in os.listdir(os.path.join(folder_path,testcase_1,testcase_2)):
            for case_file in os.listdir(os.path.join(folder_path,testcase_1,testcase_2,testcase_3)):
                testcase_name = testcase_1 + testcase_2 + testcase_3 + '/' + case_file
                #folder_casename.append(testcase_name)
                new_filenames = names_vul_dict.keys()
                for file_name in new_filenames:
                    if file_name == testcase_name:
                        #filename2 = file_name.split(' ')[0]
                        #vulline = file_name.split(' ')[1]
                        print(file_name)
                        vullines = names_vul_dict[file_name]
                        print(vullines)
                        filepath = os.path.join(folder_path,testcase_1,testcase_2,testcase_3,case_file)
                        f=open(filepath,'r')
                        sentences = f.read().split('\n')
                        for j in range(len(vullines)):
                            if int(vullines[j]) != 0 :
                                #print(sentences)
                                f.close()
                                if int(vullines[0]) == 0:
                                    i = j - 1
                                else:
                                    i = j
                                        
                                vulline = int(vullines[j]) + i*2
                                print(j)
                                print(vulline)
                                tokens = sentences[int(vulline)-1].split(' ')
                                tab_num = 0
                                for token in tokens:
                                    if token == '':
                                        tab_num = tab_num + 1
                                    strings_1 = ' ' * tab_num + 'test_insert();'
                                print(strings_1)
                                sentences.insert(int(vulline)-1,strings_1)
                                sentences.insert(int(vulline)+1,strings_1)
                        sentences.insert(-1,strings_3)
                        sentences.insert(-1,strings_2)
                        f1 = open(filepath,'w')
                        for sentence_new in sentences:
                            f1.write(sentence_new+'\n')
                        f1.close()
                                
                                        
                                     
                                    
                                    
                                                                        

                                

                                
                            