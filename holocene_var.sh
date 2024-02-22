#! /bin/bash -x

cd /work/mh0469/k203127/Holocene/Catdata/slo0042+slo0046+slo0050/echam

#for var in 143 142 151 167 165 166 164 97; do
#for var in 169; do
for var in 160; do

cdo -f nc copy slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.grb /work/bm0963/b380761/Holocene/slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc

done




