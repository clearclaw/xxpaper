#! /bin/bash

set -e

./build.sh $*
pushd build
  rsync -rav ./ claw@kanga.nu:~/public_html/xxpaper/example/
popd
