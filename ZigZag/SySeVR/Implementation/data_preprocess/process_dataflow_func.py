## coding: utf-8
'''
This python file is used to precess the vulnerability slices, including read the pkl file and split codes into corpus.
Run main function and you can get a corpus pkl file which map the same name slice file.
'''

import os
import pickle
from tkinter import N
from mapping import *



def check_label_sard(path):
    if "/home/ZigZag/Dataset/target_programs" in path:
        return "Test/Origin"
    elif "/home/ZigZag/Dataset/train_programs" in path:
        return "Train/Origin"
    elif "/home/ZigZag/ZigZag-Framework/code_transform/sard-deform/deform_dataset/test" in path:
        tigressType = path.split("/")[8]
        return "Test/" + tigressType
    elif "/home/ZigZag/ZigZag-Framework/code_transform/sard-deform/deform_dataset/train" in path:
        tigressType = path.split("/")[8]
        return "Train/" + tigressType

def check_label_nvd(path):
    if "/home/ZigZag/Dataset/real-world-programs" in path:
        software, software_version, CVE_ID = path.split("/")[5], path.split("/")[6],path.split("/")[7]
        return "Origin" + "/" + software + "/" + software_version + "/" + CVE_ID
    elif "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/deform-dataset-v3.1" in path:
        tigressType, software, software_version, CVE_ID = path.split("/")[7], path.split("/")[8], path.split("/")[9], path.split("/")[10]
        return tigressType + "/" + software + "/" + software_version + "/" + CVE_ID
'''
get_sentences function
-----------------------------
This function is used to split the slice file and split codes into words

# Arguments
    _path: String type, the src of slice files
    labelpath: String type, the src of label files
    deletepath: delete list, delete repeat slices
    corpuspath: String type, the src to save corpus
    maptype: bool type, choose do map or not
'''
def get_sentences(_path, labelpath, deletepath, corpuspath, maptype=True):

    for filename in os.listdir(_path):
        count_none = 0

        if (filename.endswith(".txt") is False):
            continue
        print(filename)

        # mkdir <corpus> for each <filename>
        corpus_path = os.path.join(corpuspath, filename[:-4])
        if os.path.exists(corpus_path) is False:
            os.system("mkdir -p " + corpus_path)

        # Read <slices>
        filepath = os.path.join(_path, filename)
        f1 = open(filepath, 'r', encoding="ISO-8859-1")
        slicelists = f1.read()
        f1.close()
        slicelists = slicelists.split('\n------------------------------\n')[:-1]

        if slicelists[0] == '':
            del slicelists[0]
        if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
            del slicelists[-1]

        # Read <delete>
        with open(os.path.join(deletepath, filename[:-4] + ".pkl"), "rb") as f:
            deletelists = pickle.load(f)

        # Read <label>
        with open(os.path.join(labelpath, filename[:-4] + "_label.pkl"), "rb") as f:
            labellists = pickle.load(f)

        print(filename + ":" + str(len(labellists) - len(deletelists)))

        del_index = -1
        for slicelist in slicelists:

            # delete
            del_index = del_index + 1
            if del_index in deletelists:
                print(del_index)
                continue

            slicefile_corpus = []
            slicefile_labels = []
            slicefile_focus = []
            slicefile_filenames = []
            slicefile_func = []

            focuspointer = None
            slice_corpus = []
            focus_index = 0
            flag_focus = 0

            # preprocess
            sentences = slicelist.split('\n')

            if sentences[0] == '\r' or sentences[0] == '':
                del sentences[0]
            if sentences == []:
                continue
            if sentences[-1] == '':
                del sentences[-1]
            if sentences[-1] == '\r':
                del sentences[-1]

            # Todo: Need to be modified.
            label_id = sentences[0].strip()
            index = sentences[0].split(" ")[0]
            path = sentences[0].split(" ")[1]
            focus = " ".join(sentences[0].split(" ")[2: -1])
            focus_line_num = sentences[0].split(" ")[-1]
            focuspointer = [focus.lstrip("[u'").rstrip("']"), focus_line_num]
            
            # key: check label function
            # key = check_label_sard(path)
            key = check_label_nvd(path)
            if key is None:
                count_none = count_none + 1
                continue
            print(focuspointer)
            print(key)

            program_id = sentences[0].split(" ")[1].split("/")[-1]

            # Handle
            sentences = sentences[1:]
            for sentence in sentences:
                if sentence.split(" ")[-1] == focuspointer[1] and flag_focus == 0:
                    flag_focus = 1
                sentence = ' '.join(sentence.split(" ")[:-1])
                start = str.find(sentence, r'printf("')
                if start != -1:
                    start = str.find(sentence, r'");')
                    sentence = sentence[:start + 2]

                fm = str.find(sentence, '/*')
                if fm != -1:
                    sentence = sentence[:fm]
                else:
                    fm = str.find(sentence, '//')
                    if fm != -1:
                        sentence = sentence[:fm]

                sentence = sentence.strip()
                list_tokens = create_tokens(sentence)

                if flag_focus == 1:
                    if "expr" in filename:
                        focus_index = focus_index + int(len(list_tokens) / 2)
                        flag_focus = 2
                        slicefile_focus.append(focus_index)
                    else:
                        if focuspointer[0] in list_tokens:
                            focus_index = focus_index + list_tokens.index(focuspointer[0])
                            flag_focus = 2
                            slicefile_focus.append(focus_index)
                        else:
                            if '*' in focuspointer[0]:
                                if focuspointer[0] in list_tokens:
                                    focus_index = focus_index + list_tokens.index(focuspointer[0].replace('*', ''))
                                    flag_focus = 2
                                    slicefile_focus.append(focus_index)
                                else:
                                    flag_focus = 0
                            else:
                                flag_focus = 0
                if flag_focus == 0:
                    focus_index = focus_index + len(list_tokens)

                if maptype:
                    slice_corpus.append(list_tokens)
                else:
                    slice_corpus = slice_corpus + list_tokens

            if flag_focus == 0:
                continue
            slicefile_labels.append(labellists[label_id])
            slicefile_filenames.append(label_id)

            if maptype:
                slice_corpus, slice_func = mapping(slice_corpus)
                slice_func = list(set(slice_func))
                if slice_func == []:
                    slice_func = ['main']
                sample_corpus = []
                for sentence in slice_corpus:
                    list_tokens = create_tokens(sentence)
                    sample_corpus = sample_corpus + list_tokens
                slicefile_corpus.append(sample_corpus)
                slicefile_func.append(slice_func)
            else:
                slicefile_corpus.append(slice_corpus)

            # save corpus
            folder_path = os.path.join(corpus_path, key, program_id)
            print(folder_path)
            if not os.path.exists(folder_path):
                os.system("mkdir -p " + folder_path)
            savefilename = index + "-" + focus_line_num + '.pkl'
            if not os.path.exists(os.path.join(folder_path, savefilename)):
                f1 = open(os.path.join(folder_path, savefilename), 'wb')
                pickle.dump([slicefile_corpus, slicefile_labels, slicefile_focus, slicefile_func, slicefile_filenames],
                            f1)
            else:
                f1 = open(os.path.join(folder_path, savefilename), 'rb')
                data = pickle.load(f1)
                f1.close()
                f1 = open(os.path.join(folder_path, savefilename), 'wb')
                pickle.dump([slicefile_corpus + data[0], slicefile_labels + data[1], slicefile_focus + data[2],
                             slicefile_func + data[3], slicefile_filenames + data[4]], f1)
            f1.close()
        print(filename + "(None):" + str(count_none))
        

if __name__ == '__main__':
    
    SLICEPATH = './data/ZigZag/slices/'
    LABELPATH = './data/ZigZag/slices/'
    DELETEPATH = './data/ZigZag/slices/delete/'
    CORPUSPATH = './data/ZigZag/slices/corpus'
    MAPTYPE = True

    sentenceDict = get_sentences(SLICEPATH, LABELPATH, DELETEPATH, CORPUSPATH, MAPTYPE)

    print('success!')