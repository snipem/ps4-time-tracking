(cd ps4-wake &&
git submodule init &&
git submodule update &&
make) &&
cp ps4-wake/ps4-wake ps4wake &&
chmod +x ps4wake &&
echo "*** Please copy ps4wake to your bin directory"

