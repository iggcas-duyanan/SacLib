FLT="-filter 0.5,20.,6"
CUT="-cut 2017,319,12,30,0. 2017,319,13,30,0."
DT="-dt 0.01"
XY="-utm 32"

./sacutils.sh -r A1.sac -w A1.Mod.sac $FLT $CUT $DT $XY