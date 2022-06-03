import os

code_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/software"
for software in os.listdir(code_path):
    for software_version in os.listdir(os.path.join(code_path, software)):
        software_version_path = os.path.join(code_path, software, software_version)
        print(software_version_path)
        if os.path.isdir(software_version_path):
            if software == "ffmpeg":
                # os.system(f"cd {software_version_path} && chmod a+x configure && ./configure")
                pass
            elif software == "imagemagick":
                os.system(f"cd {software_version_path} && chmod a+x configure && ./configure")
                pass
            elif software == "libtiff":
                os.system(f"cd {software_version_path} && chmod a+x configure && ./configure")
                pass
            elif software == "linux_kernel":
                pass
            elif software == "openssl":
                os.system(f"cd {software_version_path} && chmod a+x config && ./config")
                pass
            elif software == "wireshark":
                # os.system(f"cd {software_version_path} && chmod a+x configure && ./configure")
                pass
            else:
                print("Error")

for software in os.listdir(code_path):
    for software_version in os.listdir(os.path.join(code_path, software)):
        software_version_path = os.path.join(code_path, software, software_version)
        if os.path.isdir(software_version_path) and not os.path.exists(os.path.join(software_version_path, "config.h")):
            print("Not Config: " + software_version_path)