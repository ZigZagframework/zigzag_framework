# -*- coding:utf-8 -*-
import os
import shutil
import random
import xlrd
import pickle
import csv

def randomstr():
    Str = ' '
    i = random.randint(0,6)
    if i == 0:
        Str = 'for'
    elif i == 1:
        Str = 'goto'
    elif i == 2:
        Str = 'if'
    elif i == 3:
        Str = 'ifelse'
    elif i == 4:
        Str = 'switch0'
    elif i == 5:
        Str = 'switch1'
    elif i == 6:
        Str = 'while'
    return Str

def confusiontype4(file_path,taget_path):
    global type4_path
    command = type4_path + '/tigress --Transform=Flatten --FlattenDispatch=switch --Functions=%50 --Exclude=main --out='+ taget_path + ' ' + file_path
    os.system(command)

"""
def confusiontype3(file_path,taget_path):
    global type3_path
    command = type3_path + '/build/tooling_sample_%s '%randomstr() + file_path + ' -- >>' + taget_path
    os.system(command)

def confusiontype3_1(file_path,taget_path):
    global type3_path
    command = type3_path + '/tigress --Transform=Ident --Function=main --out='+ file_path + ' ' + taget_path
    os.system(command)
"""

def confusiontype3(file_path,taget_path,idlistpath,flag):
    global type3_path
    command ='python ' + type3_path + ' ' + file_path + ' ' + taget_path + ' ' + idlistpath + ' ' + str(flag)
    os.system(command)

def confusiontype2(file_path,taget_path):
    global type2_path
    command = type2_path +'/bin/cxx-obfus  ' + file_path + ' -o ' + taget_path + ' -n none -s none'
    os.system(command)
    f = open(taget_path)
    text = f.read()
    f.close()
    os.remove(taget_path)
    fw = open(taget_path,'w')
    for funcname in nrows:
        replace =  'ReplacementFor_' + funcname
        text = text.replace(replace,funcname)
    fw.write(text)
    fw.close()

def confusiontype1(file_path,taget_path):
    global type2_path
    command = type2_path +'/bin/cxx-obfus  ' + file_path + ' -o ' + taget_path + ' -n none -s none'
    os.system(command)
    #fw = open(taget_path,'w')
    fr = open(taget_path)
    text = fr.read()
    text = text.replace('ReplacementFor_','')
    fr.close
    os.remove(taget_path)
    fw = open(taget_path,'w')
    fw.write(text)
    fw.close

def confusion(file_path,taget_path,flag):
    global con_type
    global listpath
    if con_type == 4:
        confusiontype4(file_path,taget_path)
        print(taget_path)
        '''
        newfile = taget_path
        shutil.copy(newfile, taget_path)
        os.remove(newfile)
        '''

    elif con_type == 3:
        confusiontype3(file_path,taget_path,listpath,flag)

    elif con_type == 2:
        confusiontype2(file_path,taget_path)

    elif con_type == 1:
        confusiontype1(file_path,taget_path)
    else:
        print('error')


def Recursive_processing (file_path,taget_path,flag):
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
        for f in files:
            file_path1 = file_path + os.path.sep + f
            if os.path.isdir(file_path1):
                taget_path1 = taget_path + os.path.sep + f
                if not (os.path.exists(taget_path1)):
                    os.mkdir(taget_path1)
                Recursive_processing(file_path1,taget_path1,flag)
            else:
                taget_path1 = taget_path + os.path.sep + f
                confusion(file_path1,taget_path1,flag)
    else:
        taget_path1 = taget_path + os.path.sep + f
        confusion(file_path,taget_path1,flag)
                

global listpath
global funclist
funclist = 'cin,recv,vscanf'


global type4_path
global type2_path
global type3_path
global type3_path1
global con_type
type4_path = '/home/data/tigress-2.1'                      
#type3_path = '/home/Desktop/llvm-clang-samples-master'              
#type3_path1 = '/home/Documents/tigress-2.1'            
type3_path = 'con3.py'
type2_path = '/home/Software/Stunnix-CXX'    
con_type = 4
    
file_path = './test'
taget_path = './result'
if not (os.path.exists(taget_path)):
    os.mkdir(taget_path)
Recursive_processing(file_path,taget_path,0)
