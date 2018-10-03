#! /bin/sh

dirpath=$1
dirname=$(basename ${dirpath})
datestr=$(date +%Y%m%d)
suffix=${dirname}_${datestr}.txt

find ${dirpath} -type f -ls | tee find_${suffix} | awk '{print $11}' | xargs md5sum | tee md5sum_list_${suffix}
