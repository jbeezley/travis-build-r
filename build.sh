set -e -x
pushd "$name"
./configure "--prefix=$HOME/$prefix"
make
make check
make install
popd
echo "PATH=$HOME/$prefix/bin:$PATH" > env
