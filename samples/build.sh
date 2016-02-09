#! /bin/bash
set -e

rm -rf build || true
mkdir -p build
for xxp in *.xxp
do
  pushd build
    dirname=$(echo $xxp | sed s/-Papers.xxp//)
    mkdir -p $dirname
    pushd $dirname
      xxpaper ../../$xxp $*
      rm market_*-nooutline* || true
      cp ../../$xxp ./
      for file in *.ps
      do
        ps2pdf $file
      done
      rm *.ps
    popd
  popd
done
  