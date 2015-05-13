set -e -x
cp env "$HOME/$prefix"
tar -C "$HOME/$prefix" jcf "${name}.tar.bz2" "$name"
