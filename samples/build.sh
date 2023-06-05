#! /bin/bash
set -e

rm -rf build || true
mkdir -p build
if [ -z "${1}" ]
then
  files=*.xxp
else 
  files=${1}
fi
for xxp in ${files}
do
  pushd build
    for paper in letter A4
    do
      f=${xxp/.xxp/}
      xxpaper make assets ../$xxp -p ${paper} -c ${f}-${paper}-cutline.pdf
      xxpaper make assets ../$xxp -p ${paper} ${f}-${paper}-diecut.pdf
      cp ../$xxp ./
    done
  popd
done
  