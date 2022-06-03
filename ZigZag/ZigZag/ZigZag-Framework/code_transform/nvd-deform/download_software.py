import os
import re

download_link = dict()
download_link["imagemagick"] = "https://download.imagemagick.org/ImageMagick/download/releases/"
download_link["ffmpeg"] = "https://ffmpeg.org/releases/"
download_link["libtiff"] = "https://download.osgeo.org/libtiff/"
download_link["openssl"] = "https://www.openssl.org/source/old/"
download_link["linux_kernel"] = "https://mirrors.tuna.tsinghua.edu.cn/kernel/"
download_link["wireshark"] = "https://2.na.dl.wireshark.org/src/all-versions/"

def get_version(path, pattern):
    _version = dict()
    for _software in os.listdir(path):
        _version[_software] = set()
        _software_path = os.path.join(path, _software)
        for _dir in os.listdir(_software_path):
            _software_version = re.search(pattern, _dir).group("version")
            _version[_software].add(_software_version)
    return _version

def wget(_url, _path):
    os.system(f"wget -P {_path} {_url} --no-check-certificate")

if __name__ == "__main__":
    version = get_version("/home/ZigZag/Dataset/real-world-programs", re.compile('(?P<version>\d.*)_'))
    download_path = "/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/software"
    print(version)

    # Download
    for software in version.keys():
        save_path = f"{download_path}/{software}/"
        os.system(f"mkdir -p {save_path}")
        if software == "imagemagick":
            for v in version[software]:
                url = download_link[software] + f"ImageMagick-{v}.tar.xz"
                wget(url, save_path)
        elif software == "ffmpeg":
            for v in version[software]:
                url = download_link[software] + f"ffmpeg-{v}.tar.gz"
                wget(url, save_path)
        elif software == "libtiff":
            for v in version[software]:
                if v == '3.9.2' or v == '4.0.2':
                    url = download_link[software] + f"old/tiff-{v}.tar.gz"
                else:
                    url = download_link[software] + f"tiff-{v}.tar.gz"
                wget(url, save_path)
        elif software == "openssl":
            for v in version[software]:
                pattern = re.compile("(?P<num>\d*.\d*.\d*)")
                res = re.search(pattern, v).group("num")
                if res.startswith("0.9"):
                    url = download_link[software] + f"0.9.x/openssl-{v}.tar.gz"
                else:
                    url = download_link[software] + f"{res}/openssl-{v}.tar.gz"
                wget(url, save_path)
        elif software == "linux_kernel":
            for v in version[software]:
                res = v.split(".")[:2]
                if int("".join(res)) <= 30:
                    url = download_link[software] + f"v{res[0]}.{res[1]}/linux-{v}.tar.gz"
                else:
                    url = download_link[software] + f"v{res[0]}.x/linux-{v}.tar.gz"
                wget(url, save_path)
        elif software == "wireshark":
            for v in version[software]:
                url = download_link[software] + f"wireshark-{v}.tar.bz2"
                wget(url, save_path)
        else:
            print(">> Error!")
    print(">> Download finished.")

    # Verify
    download_version = get_version(download_path, re.compile('(?P<version>\d.*).tar'))
    print(download_version)
    verify = dict()
    for software in download_version.keys():
        verify[software] = version[software] - download_version[software]
        print(f">>> key:{software}, value:{verify[software]}")