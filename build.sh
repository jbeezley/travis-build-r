set -e -x
pushd "$srcpath"
./configure "--prefix=$HOME/$prefix"
make
make check
make install
popd
echo "PATH=$HOME/$prefix/bin:$PATH" > env
