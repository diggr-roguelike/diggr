find supercollider -type f -exec sed -i 's/CMAKE_SOURCE_DIR/CMAKE_PROJECT_DIR/g' {} +
mkdir build
cd build
cmake ..
make
make install/strip
