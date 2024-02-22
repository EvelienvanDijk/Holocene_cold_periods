#! /bin/bash -x

cd /work/bm0963/b380761/Holocene

cdo -f nc copy /pool/data/ECHAM6/post/FixCodes/F63GR15_LAND landmask.nc
cdo setctomiss,0 landmask.nc landmask_miss.nc
cdo sellonlatbox,-180,180,0,90 landmask_miss.nc landmask_miss_NH.nc
cdo sellonlatbox,-180,180,30,90 landmask_miss.nc landmask_miss_NHext.nc
cdo sellonlatbox,-10,32,35,72 landmask_miss.nc landmask_miss_Eur.nc
cdo sellonlatbox,4,32,58,72 landmask_miss.nc landmask_miss_NEur.nc
cdo sellonlatbox,0,25,37,45 landmask_miss.nc landmask_miss_SEur.nc

mv landmask*.nc landmask

for var in 167; do

cdo sellonlatbox,-180,180,0,90 slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH.nc
cdo sellonlatbox,-180,180,30,90 slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext.nc
cdo sellonlatbox,-10,32,35,72 slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur.nc
cdo sellonlatbox,4,32,58,72 slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur.nc
cdo sellonlatbox,0,25,37,45 slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur.nc

cdo yearmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_ymean.nc
cdo yearmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_ymean.nc
cdo yearmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_ymean.nc
cdo yearmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_ymean.nc
cdo yearmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_ymean.nc

cdo seasmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_seas.nc
cdo seasmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_seas.nc
cdo seasmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_seas.nc
cdo seasmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_seas.nc
cdo seasmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_seas.nc

cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_ymean.nc landmask/landmask_miss_NH.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_ym_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_seas.nc landmask/landmask_miss_NH.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_seas_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_ymean.nc landmask/landmask_miss_NHext.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_ym_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_seas.nc landmask/landmask_miss_NHext.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_seas_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_ymean.nc landmask/landmask_miss_Eur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_ym_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_seas.nc landmask/landmask_miss_Eur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_seas_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_ymean.nc landmask/landmask_miss_NEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_ym_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_seas.nc landmask/landmask_miss_NEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_seas_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_ymean.nc landmask/landmask_miss_SEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_ym_landmask.nc
cdo mul slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_seas.nc landmask/landmask_miss_SEur.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_seas_landmask.nc

cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_ym_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_ym_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_ym_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_ym_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_ym_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_ym_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_ym_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_ym_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_ym_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_ym_landmask_fm.nc

cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_seas_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NH_seas_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_seas_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NHext_seas_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_seas_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_Eur_seas_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_seas_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_NEur_seas_landmask_fm.nc
cdo fldmean slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_seas_landmask.nc slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_${var}_SEur_seas_landmask_fm.nc

done




