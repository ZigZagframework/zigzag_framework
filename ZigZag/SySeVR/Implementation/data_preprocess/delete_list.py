## coding: utf-8

import pickle
import os

def dedouble(Hashpath,Deletepath):
    for filename in os.listdir(Hashpath):
        hashpath = os.path.join(Hashpath,filename)
        f = open(hashpath,'rb')
        hashlist = pickle.load(f)
        f.close()
        print(">>> file: " + filename + ", nums(Before): " + str(len(hashlist)))
        datalist = []
        delete_list  = []
        hash_index = -1
        for data in hashlist:
            hash_index += 1
            if data not in datalist:
                datalist.append(data)
            else:
                delete_list.append(hash_index)  #index of slices to delete
        with open(os.path.join(Deletepath,filename),'wb') as f:
            pickle.dump(delete_list,f)
        print(">>> file: " + filename + ", nums(After): " + str(len(datalist)))
        f.close()

if __name__ == '__main__':
    hashpath = './data/ZigZag/slices/hash_slices'
    deletepath = './data/ZigZag/slices/delete'

    dedouble(hashpath,deletepath)