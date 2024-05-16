# Jetson Orin Considertaions

User: uc3m
Password: uc3mOrin#

# todo
git clean --force -x  -d &&git fetch && git reset --hard origin/main && git pull

install 
https://github.com/nickel110/gstthetauvc
https://codetricity.github.io/theta-linux/software/#using-gstthetauvc-to-eliminate-v4l2loopback


# Live-sharing

- [Live streaming to Jetson](https://codetricity.github.io/theta-linux/equipment/)


# Flash new Jetpack

http://www.yahboom.net/study/Jetson-Orin-NANO



## Steps to install Jetson

``` bash
sudo apt update
# sudo apt install libjpeg-dev
# sudo apt-get install libudev-dev

git clone https://github.com/ricohapi/libuvc-theta.git ~/libuvc-theta
cd ~/libuvc-theta
# REMOVE? git checkout theta_uvc

mkdir build && cd build
cmake ..
sudo make install

# sudo apt -y install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libgstreamer-plugins-base1.0-dev

git clone https://github.com/ricohapi/libuvc-theta-sample.git ~/libuvc-theta-sample
cd ~/libuvc-theta-sample/gst
make

git clone https://github.com/umlaeute/v4l2loopback.git ~/v4l2loopback
cd ~/v4l2loopback
make && sudo make install
sudo depmod -a

~/libuvc-theta-sample/gst/gst_viewer

```

