#! /bin/bash -x

cd /work/bm0963/from_Mistral/bm0963/b380761/Holocene/novolc

#for var in 143 142 151 167 165 166 164 97; do
for var in 160; do

cdo -f nc copy slo0043_echam6_BOT_mm_1001-8850_${var}.grb slo0043_echam6_BOT_mm_1001-8850_${var}.nc

done




