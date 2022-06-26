## coding:utf-8
import os
import pickle
import argparse

def make_label(path, _dict):
    print(path)
    f = open(path, 'r', encoding="ISO-8859-1")
    slicelists = f.read()
    f.close()
    slicelists = slicelists.split('\n------------------------------\n')[:-1]

    labels = dict()
    if slicelists[0] == '':
        del slicelists[0]
    if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
        del slicelists[-1]

    for slicelist in slicelists:
        sentences = slicelist.split('\n')

        if sentences[0] == '\r' or sentences[0] == '':
            del sentences[0]
        if sentences == []:
            continue
        if sentences[-1] == '':
            del sentences[-1]
        if sentences[-1] == '\r':
            del sentences[-1]

        slicename = sentences[0].split(' ')[1] # dict_key
        label_key = sentences[0].strip()
        print("dict_key: " + slicename)
        print("label_key: " + label_key)
        sentences = sentences[1:]

        label = 0

        if slicename not in _dict.keys():
            labels[label_key] = label
            continue
        else:
            vulline_nums = _dict[slicename]
            vulline_nums = [str(x) for x in vulline_nums]
            print("vulline_nums: ")
            print(vulline_nums)
            for sentence in sentences:
                if (is_number(sentence.split(' ')[-1])) is False:
                    continue
                linenum = str(sentence.split(' ')[-1])
                # print("linenum: ")
                # print(linenum)
                if linenum not in vulline_nums:
                    # print("not in")
                    continue
                else:
                    # print("in")
                    label = 1
                    break
            labels[label_key] = label
            print("Label: " + str(label))
    return labels


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pkl", nargs='*', required=True, help="Label PKL File")
    parameters = parser.parse_args()
    _dict = dict()
    for _pkl in parameters.pkl:
        with open(_pkl, 'rb') as f:
            temp = pickle.load(f)
            _dict.update(temp)

    lang = './data/ZigZag/slices'

    path = os.path.join(lang, 'api_slices.txt')
    list_all_apilabel = make_label(path, _dict)
    dec_path = os.path.join(lang, 'api_slices_label.pkl')
    f = open(dec_path, 'wb')
    pickle.dump(list_all_apilabel, f, True)
    f.close()

    path = os.path.join(lang, 'array_slices.txt')
    list_all_arraylabel = make_label(path, _dict)
    dec_path = os.path.join(lang, 'array_slices_label.pkl')
    f = open(dec_path, 'wb')
    pickle.dump(list_all_arraylabel, f, True)
    f.close()

    path = os.path.join(lang, 'pointer_slices.txt')
    list_all_pointerlabel = make_label(path, _dict)
    dec_path = os.path.join(lang, 'pointer_slices_label.pkl')
    f = open(dec_path, 'wb')
    pickle.dump(list_all_pointerlabel, f, True)
    f.close()
 
    path = os.path.join(lang, 'expr_slices.txt')
    list_all_exprlabel = make_label(path, _dict)
    dec_path = os.path.join(lang, 'expr_slices_label.pkl')
    f = open(dec_path, 'wb')
    pickle.dump(list_all_exprlabel, f, True)
    f.close()


if __name__ == '__main__':
    main()
    print(">>> Finished!")
