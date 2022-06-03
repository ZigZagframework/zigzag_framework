
import os
import subprocess
import pickle
import sys
import re
from threading import Timer

def print_log(_string, _file):
    print(_string)
    print(_string, file=_file)

def kill_command(p):
    p.kill()

def run(_command, _log):
    p = subprocess.Popen(_command, shell=True, stdout=_log, stderr=subprocess.STDOUT)
    return_code = -1
    timer = Timer(20, kill_command, [p]) # after 20s kill process
    try:
        timer.start()
        return_code = p.wait()
    except Exception as ex:
        print(ex)
    finally:
        timer.cancel()
    _log.flush()
    return return_code

def trans_data(code_path, deform_path, software_path, vul_func_path, _type, log):
    cmd_head = ""
    cmdHead1 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=EncodeLiterals --EncodeLiteralsKinds=string --Functions='
    cmdHead2 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=RndArgs --RndArgsBogusNo=1 --Functions='
    cmdHead3 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Flatten --Functions='
    cmdHead4 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Merge --Functions='
    cmdHead5 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Merge --Functions='
    cmdHead6 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Split --Seed=0 --SplitKinds=top --SplitCount=2 --Functions='
    cmdHead7 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Split --Seed=0 --SplitKinds=block --SplitCount=2 --Functions='
    cmdHead8 = 'tigress --Environment=x86_64:Linux:Gcc:4.6 --Transform=Split --Seed=0 --SplitKinds=recursive --SplitCount=2 --Functions='

    cmdMiddle3 = ' --FlattenDispatch=switch --out='
    cmdMiddle5 = ' --MergeFlatten=true --out='

    if _type == 1:
        cmd_head = cmdHead1
    elif _type == 2:
        cmd_head = cmdHead2
    elif _type == 3:
        cmd_head = cmdHead3
    elif _type == 4:
        cmd_head = cmdHead4
    elif _type == 5:
        cmd_head = cmdHead5
    elif _type == 6:
        cmd_head = cmdHead6
    elif _type == 7:
        cmd_head = cmdHead7
    elif _type == 8:
        cmd_head = cmdHead8

    tigress_type = "tigressType" + str(_type)
    cmd_dependency = ""
    for software in os.listdir(code_path):
        for software_version in os.listdir(os.path.join(code_path, software)):
            version = re.search(re.compile('(?P<version>\d.*)_'), software_version).group("version")
            corresponding = os.path.join(software_path, software)
            if software == 'ffmpeg':
                if version == "3.5":
                    version = "3.4"
                if version == "0.10.6+":
                    version = "0.10.16"
                corresponding = os.path.join(corresponding, f"ffmpeg-{version}")
                if int("".join(version.split(".")[:2])) < 40:
                    cmd_dependency = f' -I {corresponding} -I {corresponding}/libavcodec' \
                                     f' -I {corresponding}/libavformat -I {corresponding}/libavfilter' \
                                     f' -I {corresponding}/libswscale -I {corresponding}/libswresample' \
                                     f' -I {corresponding}/libavutil -include {corresponding}/libavutil/internal.h' \
                                     f' -I /usr/include/glib-2.0/  $(pkg-config --cflags glib-2.0)'
                else:
                    cmd_dependency = f' -I {corresponding} -I {corresponding}/libavcodec' \
                                     f' -I {corresponding}/libavformat -I {corresponding}/libavfilter' \
                                     f' -I {corresponding}/libswscale -I {corresponding}/libswresample' \
                                     f' -I {corresponding}/libavutil -include {corresponding}/libavutil/internal.h' \
                                     f' -include {corresponding}/compat/atomics/gcc/stdatomic.h' \
                                     f' -I {corresponding}/compat/atomics/gcc/' \
                                     f' -I /usr/include/glib-2.0/  $(pkg-config --cflags glib-2.0)'
            elif software == 'imagemagick':
                if version == "7.0.9-1":
                    version = "7.0.9-2"
                if version == "7.0.8-50" or version == "7.0.8-4":
                    version = "7.0.8-68"
                if version == "7.0.6-1":
                    version = "7.0.6-10"
                if version == "7.0.3-1":
                    version = "7.0.3-10"
                if version == "7.0.1-0":
                    version = "7.0.1-10"
                corresponding = os.path.join(corresponding, f"ImageMagick-{version}")
                cmd_dependency = f' -I {corresponding} -I {corresponding}/Magick++/lib/' \
                                 f' -I /usr/include/libxml2/'
            elif software == 'libtiff':
                corresponding = os.path.join(corresponding, f"tiff-{version}")
                cmd_dependency = f" -I {corresponding} -I {corresponding}/libtiff/"
            elif software == 'openssl':
                corresponding = os.path.join(corresponding, f"openssl-{version}")
                cmd_dependency = f" -I {corresponding} -I {corresponding}/include/ -I {corresponding}/crypto/" \
                                 f" -I {corresponding}/ssl"
                for __import in os.listdir(os.path.join(corresponding, "crypto")):
                    __path = os.path.join(corresponding, "crypto", __import)
                    if os.path.isdir(__path):
                        cmd_dependency = cmd_dependency + " -I " + __path
            elif software == 'linux_kernel':
                corresponding = os.path.join(corresponding, f"linux-{version}")
                if int("".join(version.split(".")[:3])) < 2635:
                    cmd_dependency = f" -nostdinc -isystem /usr/lib/gcc/x86_64-linux-gnu/5.4.0/include" \
                                     f" -I {corresponding}/arch/x86/include -I {corresponding}/include" \
                                     f" -I {corresponding}/arch/x86/include/asm/" \
                                     f" -I {corresponding}/kernel" \
                                     f" -I {corresponding}/include/linux" \
                                     f" -include {corresponding}/include/linux/autoconf.h -D__KERNEL__"
                else:
                    cmd_dependency = f" -nostdinc -isystem /usr/lib/gcc/x86_64-linux-gnu/5.4.0/include" \
                                     f" -I {corresponding}/arch/x86/include -I {corresponding}/include" \
                                     f" -I {corresponding}/arch/x86/include/asm/" \
                                     f" -I {corresponding}/kernel" \
                                     f" -I {corresponding}/include/generated" \
                                     f" -include {corresponding}/include/generated/autoconf.h -D__KERNEL__"
            elif software == 'wireshark':
                if version == "1.12.14":
                    version = '1.12.13'
                corresponding = os.path.join(corresponding, f"wireshark-{version}")
                cmd_dependency = f' -I {corresponding} -I {corresponding}/wiretap/ -I {corresponding}/epan/' \
                                 f' -I {corresponding}/epan/dissectors/ -I {corresponding}/epan/wmem/' \
                                 f' -I {corresponding}/plugins/irda/ -I {corresponding}/plugins/profinet/' \
                                 f' -I {corresponding}/plugins/docsis/ -I {corresponding}/plugins/ethercat/' \
                                 f' -I {corresponding}/wsutil -I {corresponding}/wiretap' \
                                 f' -I /usr/include/glib-2.0/ $(pkg-config --cflags glib-2.0)'
            else:
                print_log("Software Error", log)
            for cve_id in os.listdir(os.path.join(code_path, software, software_version)):
                for _dir in os.listdir(os.path.join(code_path, software, software_version, cve_id)):
                    for filename in os.listdir(os.path.join(code_path, software, software_version, cve_id, _dir)):
                        print_log('\n', log)
                        os.system(f"mkdir -p {os.path.join(deform_path, tigress_type, software, software_version, cve_id, _dir)}")
                        old_file = os.path.join(code_path, software, software_version, cve_id, _dir, filename)
                        new_file = os.path.join(deform_path, tigress_type, software, software_version, cve_id, _dir, filename)
                        print_log(f'>>> Origin:{old_file}', log)
                        print_log(f'>>> New:{new_file}', log)
                        for vul_funcs in os.listdir(os.path.join(vul_func_path, software, cve_id)):
                            commit_hash = _dir.split("_")[2]
                            if commit_hash in vul_funcs:
                                pattern_vul_func = re.compile("\.c[0-9_.]*(?P<vul_func>.*?)_OLD")
                                res = re.search(pattern_vul_func, vul_funcs)
                                if res is None:
                                    print_log(f">>> Empty vul func: {vul_funcs}", log)
                                    continue
                                else:
                                    func = res.group("vul_func")
                                if _type == 3:
                                    cmd = cmd_head + func + cmdMiddle3 + new_file + f'#{func}#.c ' + old_file + cmd_dependency
                                elif _type == 4:
                                    cmd = cmd_head + func + ',%10' + ' --out=' + new_file + f'#{func}#.c ' + old_file + cmd_dependency
                                elif _type == 5:
                                    cmd = cmd_head + func + ',%10' + cmdMiddle5 + new_file + f'#{func}#.c ' + old_file + cmd_dependency
                                else:
                                    cmd = cmd_head + func + ' --out=' + new_file + f'#{func}#.c ' + old_file + cmd_dependency
                                print_log(f">>> Tigress: {cmd}", log)
                                run(cmd, log)

def deleteNull(deform_path, _log):
    nullCount = 0
    count = 0

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
                        print_log('Empty: ' + fileDir, _log)
                        os.remove(fileDir)
                        nullCount = nullCount + 1
                    else:
                        count = count  +1
                for dirname in dirnames:
                    if not os.listdir(os.path.join(parent, dirname)):
                        print(os.path.join(parent, dirname))
                        os.rmdir(os.path.join(parent, dirname))

    print_log("nullCount : " + str(nullCount), _log)
    print_log("count :" + str(count), _log)


def main():
    code_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/insert-dataset"
    deform_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/deform-dataset-v3.1"
    software_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/software"
    vul_func_path = "/home/ZigZag/Dataset/funcs/C-Vulnerable_Funcs"
    log = open("/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/tigress4.log", "w")


    for types in range(1, 9):
        trans_data(code_path, deform_path, software_path, vul_func_path, types, log)

    deleteNull(deform_path, log)
    log.close()

if __name__ == '__main__':
    main()