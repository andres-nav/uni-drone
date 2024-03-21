

- [Live streaming to Jetson](https://codetricity.github.io/theta-linux/equipment/)

## Steps to install Jetson

``` sh
sudo apt update
git clone https://github.com/ricohapi/libuvc-theta.git ~/libuvc-theta
cd ~/libuvc-theta
git checkout theta_uvc

mkdir build && cd build
cmake ..
sudo make install

git clone https://github.com/ricohapi/libuvc-theta-sample.git ~/libuvc-theta-sample
cd ~/libuvc-theta-sample/gst
make
~/libuvc-theta-sample/gst/gst_viewer

```

