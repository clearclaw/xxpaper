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
      rm -rf $dirname || true
      mkdir -p $dirname
      pushd $dirname
        xxpaper ../../$xxp -P ${paper} $*
        rm market_*-nooutline* || true
        cp ../../$xxp ./
        for file in *.ps
        do
          ps2pdf $file
        done
        rm *.ps
      popd
      tar zcf ${dirname}-${paper}.tar.gz ${dirname}
    done
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
  