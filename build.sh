set -e -x
pushd "$srcpath"
./configure "--prefix=$HOME/$prefix"
make
make check
make install
popd
