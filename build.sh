set -e -x
pushd "$srcpath"
./configure "--prefix=$HOME/$prefix" "--enable-R-shlib"
make
make check
make install
popd
