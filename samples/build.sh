#! /bin/bash
set -e

rm -rf build || true
mkdir -p build
for xxp in *.xxp
do
  pushd build
    dirname=$(echo $xxp | sed s/-Papers.xxp//)
    for paper in letter A4
    do
      xxpaper make assets ../$xxp -p ${paper} -c $* ${xxp/.xxp/-cutline.pdf}
      xxpaper make assets ../$xxp -p ${paper} $* ${xxp/.xxp/-diecut.pdf}
      cp ../$xxp ./
    done
  popd
done
  