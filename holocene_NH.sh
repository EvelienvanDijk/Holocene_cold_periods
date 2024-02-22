#! /bin/bash -x

cd /work/bm0963/b380761/Holocene

for var in 143 142 151 167 165 166 164 97; do

cdo sellonlatbox,-180,180,0,90 slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH.nc
cdo yearmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_ymean.nc

done




