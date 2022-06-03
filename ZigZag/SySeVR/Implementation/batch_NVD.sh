#!/usr/bin/env bash

python2 batch_source2slice_NVD.py -d /home/ZigZag/Dataset/real-world-programs -l /home/SySeVR/Implementation/source2slice/log/nvd/origin

DirPath="/home/ZigZag/ZigZag-Framework/code_transform/nvd-deform/deform-dataset-v3.1"
LogPath="/home/SySeVR/Implementation/source2slice/log/nvd"
dirList="ls $DirPath"
for dir in $(eval "$dirList");
do
  python2 batch_source2slice_NVD.py -d "$DirPath/$dir" -l "$LogPath/$dir"
  echo "> Finish: $dir"
done
echo "> Done."