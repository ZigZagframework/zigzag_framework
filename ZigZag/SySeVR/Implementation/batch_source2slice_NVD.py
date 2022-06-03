import os
import pickle
import subprocess
import sys
import argparse

start_neo4j_command = "cd /home/SySeVR/neo4j/bin && ./neo4j start-no-wait && sleep 30s"
stop_neo4j_command = "cd /home/SySeVR/neo4j/bin && ./neo4j stop && sleep 10s"
clear_command = "rm -rf /home/SySeVR/joern-0.3.1/.joernIndex"

batch_info = "/home/SySeVR/Implementation/source2slice/batch_info.pkl"


def mkdir(path):
    if os.path.exists(path):
        os.system("rm -rf " + path)
    os.system("mkdir -p " + path)


def mkdir_once(path):
    if os.path.exists(path) is False:
        os.system("mkdir -p " + path)


def run(_command, _log):
    with open(_log, "w") as _f:
        pro = subprocess.Popen(_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for out in iter(pro.stdout.readline, ''):
            sys.stdout.write(out)
            _f.write(out)


if __name__ == "__main__":

    # Parser parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, help="Dataset Dir", required=True)
    parser.add_argument('-l', '--log', type=str, help="Log Dir", required=True)
    parameters = parser.parse_args()

    dataset = parameters.directory
    log_dir = parameters.log

    # Preprocess
    hint = "> Handle SARD dataset, DIR=" + dataset + ", LOG_DIR=" + log_dir
    split = "-" * len(hint)
    print split
    print hint

    mkdir_once(log_dir)
    os.system(stop_neo4j_command)
    os.system(clear_command)

    # Load handled batch info
    if os.path.exists(batch_info):
        with open(batch_info, "rb") as f:
            dirs = pickle.load(f)
            print dirs
    else:
        dirs = list()

    # Handle batch
    for testcase1 in os.listdir(dataset):
        for testcase2 in os.listdir(os.path.join(dataset, testcase1)):

            batch_dir = os.path.join(dataset, testcase1, testcase2)
            batch_log_dir = os.path.join(log_dir, testcase1, testcase2)

            if batch_dir in dirs:
                print ">>> Pass: " + batch_dir
                continue

            # if "imagemagick" in batch_log_dir:
            #     print "pass imagemagick"
            #     continue

            if "libtiff-4.0.6_vul" in batch_log_dir or "libtiff-4.0.7_novul" in batch_log_dir:
                print "pass libtiff"
                continue

            if "openssl-1.0.2_vul" in batch_log_dir:
                print "pass openssl"
                continue

            if "tigressType5/ffmpeg/ffmpeg-2.8.7_novul" in batch_dir:
                # tigress 5 "/CVE-2016-2329/CVE-2016-2329_CWE-119_89f464e9c229006e16f6bb5403c5529fdd0a9edd_tiff.c_1.1/CVE-2016-2329_CWE-119_libavcodec_tiff.c_1.1_NEW.c#tiff_decode_tag#.c"
                print "pass ffmpeg"
                continue

            mkdir(batch_log_dir)
            print split
            print "> Start: " + batch_dir + ", joern index..."

            # joern index operation
            import_command = 'JOERN="/home/SySeVR/joern-0.3.1" && ' \
                             'CodeDirectory=' + batch_dir + ' && ' \
                             'java -jar $JOERN/bin/joern.jar $CodeDirectory  -outdir $JOERN/.joernIndex'
            run(import_command, os.path.join(batch_log_dir, "joern-import.log"))
            os.system(start_neo4j_command)

            # handle SySeVR source2slice
            source2slice = "/home/SySeVR/Implementation/source2slice"
            cd_code_dir_command = "cd " + source2slice + " && "

            print "> ** Start Step 1: get_cfg_relation.py"
            mkdir(os.path.join(source2slice, "cfg_db"))
            run(cd_code_dir_command + "python2 get_cfg_relation.py",
                os.path.join(batch_log_dir, "get_cfg_relation.log"))
            print "> ** End Step 1: get_cfg_relation.py"

            print "> ** Start Step 2: complete_PDG.py"
            mkdir(os.path.join(source2slice, "pdg_db"))
            run(cd_code_dir_command + "python2 complete_PDG.py",
                os.path.join(batch_log_dir, "complete_PDG.log"))
            print "> ** End Step 2: complete_PDG.py"

            print "> ** Start Step 3: access_db_operate.py"
            mkdir(os.path.join(source2slice, "dict_call2cfgNodeID_funcID"))
            run(cd_code_dir_command + "python2 access_db_operate.py ",
                os.path.join(batch_log_dir, "access_db_operate.log"))
            print "> ** End Step 3: access_db_operate.py"

            print "> ** Start Step 4: points_get.py"
            run(cd_code_dir_command + "python2 points_get.py",
                os.path.join(batch_log_dir, "points_get.log"))
            print "> ** End Step 4: points_get.py"

            print "> ** Start Step 5: extract_df.py"
            mkdir_once(os.path.join(source2slice, "slices"))
            run(cd_code_dir_command + "python2 extract_df.py",
                os.path.join(batch_log_dir, "extract_df.log"))
            print "> ** End Step 5: extract_df.py"

            # Save batch info
            dirs.append(batch_dir)
            with open(batch_info, "wb") as f:
                pickle.dump(dirs, f)

            # print "> ** Start Step 6: make_label_sard.py"
            # mkdir(os.path.join(source2slice, "label_source"))
            # ret = run(cd_code_dir_command + "python2 make_label_sard.py")
            # with open(os.path.join(batch_log_dir, "make_label_sard.log"), "w") as f:
            #     f.writelines(ret)
            # print "> ** End Step 6: make_label_sard.py"
            #
            # print "> ** Start Step 7: data_preprocess.py"
            # mkdir(os.path.join(source2slice, "slice_label"))
            # ret = run(cd_code_dir_command + "python2 data_preprocess.py")
            # with open(os.path.join(batch_log_dir, "data_preprocess.log"), "w") as f:
            #     f.writelines(ret)
            # print "> ** End Step 7: data_preprocess.py"

            # clear operation
            os.system(stop_neo4j_command)
            os.system(clear_command)
            print "> Finished: " + batch_dir
            print split
    print "> Finished: " + dataset
