## coding:utf-8
import os

#tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=EncodeLiterals --EncodeLiteralsKinds=string --Functions=* --out=output.c input.c
import sys


def trans_data(code_path, deform_path, type):
    tigressTyprDir = os.path.join(deform_path, 'tigressType' + str(type))
    if not os.path.exists(tigressTyprDir):
        os.mkdir(tigressTyprDir)
        print("type:" + str(type))
    
    cmdHead = ""
    cmdHead1 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=EncodeLiterals --EncodeLiteralsKinds=string --Functions=\* --out='
    cmdHead2 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=RndArgs --RndArgsBogusNo=1 --Functions=\* --Exclude=main --out='
    cmdHead3 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Flatten --Functions=%50 --Exclude=main --FlattenDispatch=switch --out='
    cmdHead4 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Merge --Functions=%50 --Exclude=main --out='
    cmdHead5 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Merge --Functions=%50 --Exclude=main --MergeFlatten=true --out='
    cmdHead6 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Split --Seed=0 --SplitKinds=top --SplitCount=2 --Functions=%50 --Exclude=main --out='
    cmdHead7 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Split --Seed=0 --SplitKinds=block --SplitCount=2 --Functions=%50 --Exclude=main --out='
    cmdHead8 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Split --Seed=0 --SplitKinds=recursive --SplitCount=2 --Functions=%50 --Exclude=main --out='

    if type == 1:
        cmdHead = cmdHead1
    elif type == 2:
        cmdHead = cmdHead2
    elif type == 3:
        cmdHead = cmdHead3
    elif type == 4:
        cmdHead = cmdHead4
    elif type == 5:
        cmdHead = cmdHead5
    elif type == 6:
        cmdHead = cmdHead6
    elif type == 7:
        cmdHead = cmdHead7
    elif type == 8:
        cmdHead = cmdHead8

    folder_path = code_path
    # for folder_1 in os.listdir(code_path):
    for testcase_1 in os.listdir(folder_path):
        for testcase_2 in os.listdir(os.path.join(folder_path, testcase_1)):
            for testcase_3 in os.listdir(os.path.join(folder_path, testcase_1, testcase_2)):
                new_path = os.path.join(tigressTyprDir,testcase_1,testcase_2,testcase_3)
                if not os.path.exists(new_path):
                    cmd = "mkdir -p " + new_path
                    os.system(cmd)
                    print cmd
                for filename in os.listdir(os.path.join(code_path,testcase_1,testcase_2,testcase_3)):
                    oldfile = os.path.join(code_path,testcase_1,testcase_2,testcase_3,filename)
                    newfile = os.path.join(new_path, filename)
                    if oldfile.endswith('.c'):
                        cmd = cmdHead + newfile + ' ' + oldfile + ' -I /home/ZigZag/ZigZag-Framework/code_transform/sard-deform/shared/108'
                        print cmd
                        os.system(cmd)
                    # else:
                    #     cmd = 'cp ' +  oldfile + ' ' + newfile
                    #     print cmd
                    #     os.system(cmd)

def deleteNull(deform_path):
    nullCount = 0  # 为空的c文件总个数
    count = 0      # 不为空的文件总个数

    code_path = deform_path

    childerfolders = os.listdir(code_path)

    for childerfolder in childerfolders:
        if 'tigressType' in childerfolder:
            for parent, dirnames, filenames in os.walk(os.path.join(code_path, childerfolder)):
                for filename in filenames:
                    fileDir = os.path.join(parent, filename)
                    print(fileDir)
                    size = os.path.getsize(fileDir)
                    if size == 0:
                        print('文件是空的')
                        os.remove(fileDir)
                        nullCount = nullCount + 1
                    else:
                        count = count  +1
                for dirname in dirnames:
                    if not os.listdir(os.path.join(parent, dirname)):
                        print os.path.join(parent, dirname)
                        os.rmdir(os.path.join(parent, dirname))

    print("nullCount : " + str(nullCount))
    print("count :" + str(count))


def main():

    code_path = sys.argv[1]
    deform_path = sys.argv[2]

    for types in range(1,9):
        trans_data(code_path,deform_path,types)
    
    deleteNull(deform_path)
    

if __name__ == '__main__':
    main()