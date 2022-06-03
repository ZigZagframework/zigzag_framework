#!/usr/bin/env bash

python2 batch_source2slice_SARD.py -d /home/ZigZag/Dataset/train_programs/SARD -l /home/SySeVR/Implementation/source2slice/log/train/origin
python2 batch_source2slice_SARD.py -d /home/ZigZag/Dataset/target_programs/SARD -l /home/SySeVR/Implementation/source2slice/log/test/origin

DirPath="/home/ZigZag/ZigZag-Framework/code_transform/sard-deform/deform_dataset/train"
LogPath="/home/SySeVR/Implementation/source2slice/log/train"
dirList="ls $DirPath"
for dir in $(eval "$dirList");
do
  python2 batch_source2slice_SARD.py -d "$DirPath/$dir" -l "$LogPath/$dir"
  echo "> Finish: $dir"
done
echo "> Done."


DirPath="/home/ZigZag/ZigZag-Framework/code_transform/sard-deform/deform_dataset/test"
LogPath="/home/SySeVR/Implementation/source2slice/log/test"
dirList="ls $DirPath"
for dir in $(eval "$dirList");
do
  python2 batch_source2slice_SARD.py -d "$DirPath/$dir" -l "$LogPath/$dir"
  echo "> Finish: $dir"
done
echo "> Done."