# -*- coding: utf-8 -*-

from __future__ import print_function
import pickle
import os
import sys

diffcase = []
testcase = []


def print_log(_string, _file):
    print(_string)
    print(_string, file=_file)

def get_successive(_list):
    res = []
    for index in range(len(_list)):
        if not res:
            res.append([_list[index]])
        elif _list[index - 1] + 1 == _list[index]:
            res[-1].append(_list[index])
        else:
            res.append([_list[index]])
    return res

if __name__ == "__main__":
    f = open(sys.argv[1], 'rb')
    names_vul_dict = pickle.load(f)
    f.close()

    code_path = sys.argv[2]
    save_path = sys.argv[3]
    log_path = sys.argv[4]

    os.system("rm -rf " + save_path)
    os.system("rm -rf " + log_path)

    log = open(log_path, "w")

    strings_2 = '/*Insert_confusion_labels_2021_12*/'
    strings_3 = 'void test_insert(void){}'
    count_vul = 0
    count_non_vul = 0
    count_err = 0
    for folder_1 in os.listdir(code_path):
        for folder_2 in os.listdir(os.path.join(code_path, folder_1)):
            for folder_3 in os.listdir(os.path.join(code_path, folder_1, folder_2)):
                for folder_4 in os.listdir(os.path.join(code_path, folder_1, folder_2, folder_3)):
                    for filename in os.listdir(os.path.join(code_path, folder_1, folder_2, folder_3, folder_4)):
                        os.system("mkdir -p " + os.path.join(save_path, folder_1, folder_2, folder_3, folder_4))
                        old_key =os.path.join(code_path, folder_1, folder_2, folder_3, folder_4, filename)
                        new_key = os.path.join(save_path, folder_1, folder_2, folder_3, folder_4, filename)
                        print_log("OLD: " + old_key, log)
                        with open(old_key, "r") as f:
                            sentences = f.read().split('\n')
                        if old_key in names_vul_dict.keys():
                            count_vul = count_vul + 1
                            vullines = list(int(x) for x in names_vul_dict[old_key])
                            vullines.sort()
                            print_log("Before filter:", log)
                            print_log(vullines, log)

                            # Filter
                            for vulline in vullines[:]:
                                sentence = sentences[vulline - 1]
                                if sentence.startswith(" *") or sentence.strip() == '' or sentence.strip().startswith(("{", "}", ";")) or sentence.endswith("}"):
                                    vullines.remove(vulline)
                                    print_log("Remove 1: " + str(vulline) + ">" + sentence, log)
                                elif 'if (' in sentence or 'if(' in sentence or 'else' in sentence:
                                    vullines.remove(vulline)
                                    print_log("Remove 2: " + str(vulline) + ">" + sentence, log)

                            temp = get_successive(vullines)
                            for each in temp:
                                if len(each) == 1:
                                    vulline = each[0]
                                    sentence = sentences[vulline - 1]
                                    if "/*" not in sentence and "*/" in sentence:
                                        vullines.remove(vulline)
                                        print_log("Remove 3: " + str(vulline) + ">" + sentence, log)
                                    elif sentence.strip().startswith(",") or sentence.strip().endswith(","):
                                        vullines.remove(vulline)
                                        print_log("Remove 4: " + str(vulline) + ">" + sentence, log)
                                    elif ";" not in sentence:
                                        vullines.remove(vulline)
                                        print_log("Remove 5: " + str(vulline) + ">" + sentence, log)
                                    elif ")" in sentence and ";" in sentence and "(" not in sentence:
                                        vullines.remove(vulline)
                                        print_log("Remove 6: " + str(vulline) + ">" + sentence, log)
                                    elif "/*" in sentence and "*/" in sentence:
                                        if sentence.strip().split("/*")[0] == '':
                                            vullines.remove(vulline)
                                            print_log("Remove 7: " + str(vulline) + ">" + sentence, log)
                                elif len(each) > 1:
                                    start = each[0]
                                    end = each[-1]
                                    vul_sentence = ''.join(sentences[start - 1:end])
                                    if vul_sentence.strip().endswith(","):
                                        for vulline in each[::-1]:
                                            sentence = sentences[vulline - 1]
                                            if ";" not in sentence:
                                                vullines.remove(vulline)
                                                print_log("Remove 8: " + str(vulline) + ">" + sentence, log)
                                            else:
                                                break
                                    flag = False
                                    for vulline in each[:]:
                                        sentence = sentences[vulline - 1]
                                        if vulline not in vullines:
                                            continue
                                        if "/*" in sentence and "*/" in sentence:
                                            if sentence.strip().split("/*")[0] != '':
                                                continue
                                        if flag:
                                            vullines.remove(vulline)
                                            print_log("Remove 9: " + str(vulline) + ">" + sentence, log)
                                        if "/*" in sentence and not flag:
                                            flag = True
                                            vullines.remove(vulline)
                                            print_log("Remove 9: " + str(vulline) + ">" + sentence, log)
                                        if "*/" in sentence and flag:
                                            if vulline in vullines:
                                                vullines.remove(vulline)
                                                print_log("Remove 9: " + str(vulline) + ">" + sentence, log)
                                            flag = False
                                    for vulline in each[:]:
                                        sentence = sentences[vulline - 1]
                                        if vulline not in vullines:
                                            continue
                                        if ";" in sentence:
                                            break
                                        if sentence.strip().startswith(","):
                                            vullines.remove(vulline)
                                            print_log("Remove 10: " + str(vulline) + ">" + sentence, log)



                                # if 'if' in sentence or 'else' in sentence:
                                #     if '{' in sentences[vulline]:
                                #         vullines.remove(vulline)
                                #         print_log("Remove: " + str(vulline) + ">" + sentence, log)
                                # elif sentence.startswith(" *") or sentence.strip() == '' or sentence.strip().startswith(("{", "}", "/*", ";", ",")) or sentence.strip().endswith(("*/", ",")) or sentences[vulline -2].strip().endswith(","):
                                #     vullines.remove(vulline)
                                #     print_log("Remove: " + str(vulline) + ">" + sentence, log)

                            if len(vullines) == 0:
                                diffcase.append(os.path.join("/home/ZigZag/Dataset/diffs", folder_1, folder_2, folder_3, folder_4 + ".diff"))
                                testcase.append(old_key)

                            print_log("After filter: ", log)
                            print_log(vullines, log)

                            res = get_successive(vullines)
                            count = 0
                            for each in res:
                                start = each[0]
                                end = each[-1]
                                strings_1 = 'test_insert();'
                                sentences.insert(start - 1, strings_1)
                                sentences.insert(end + 1, strings_1)
                                count = count + 1

                            sentences.insert(-1 ,strings_2)
                            for i in range(0, len(sentences)):
                                # Find the end of #include
                                if sentences[i].startswith((" *", "/*")):
                                    continue
                                if sentences[i].startswith('#include') and sentences[i + 1].startswith('#include'):
                                    continue
                                elif sentences[i].startswith('#include') and not sentences[i + 1].startswith('#include'):
                                    sentences.insert(i + 1, strings_3)
                                    break
                        else:
                            count_non_vul = count_non_vul + 1
                        f1 = open(new_key,'w')
                        for sentence_new in sentences:
                            f1.write(sentence_new+'\n')
                        f1.close()
    for diff,testcase in zip(diffcase, testcase):
        print_log("Diff: " + diff, log)
        print_log("Testcase: " + testcase, log)
    with open("./Invalid_file.pkl", "wb") as f:
        pickle.dump(testcase, f)
    print_log("Invalid File: " + str(len(diffcase)), log)
    print_log("Vul File: " + str(count_vul), log)
    print_log("Non-Vul File: " + str(count_non_vul), log)
    print_log("Err File: " + str(count_err), log)
    log.close()

                                         
                                                                        

                                

                                
                            