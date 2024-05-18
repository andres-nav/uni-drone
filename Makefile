PWD		:= $(shell pwd)
MAKE		:= /usr/bin/make
CMAKE		:= /usr/bin/cmake
AUTORECONF	:= /usr/bin/autoreconf
LIBUVC_THETA_DIR := $(PWD)/libuvc-theta
LIBUVC_THETA_BUILD_DIR := $(LIBUVC_THETA_DIR)/build
LIBUVC_THETA_SAMPLE_DIR := $(PWD)/libuvc-theta-sample/gst
V4L2LOOPBACK_DIR := $(PWD)/v4l2loopback
GSTTHETAUVC_DIR := $(PWD)/gstthetauvc/thetauvc
OPENCV_DIR := $(PWD)/opencv

.PHONY: all
all: run

.PHONY: install
install: clean install-basic install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback install-gstthetauvc install-opencv
	@echo "Installation completed."

.PHONY: viewer
viewer:
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_viewer

.PHONY: loopback
loopback:
	$(LIBUVC_THETA_SAMPLE_DIR)/../scripts/set_v4l.sh
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_loopback

.PHONY: gstthetauvc
gstthetauvc:
	gst-launch-1.0 thetauvcsrc mode=4K ! queue ! h264parse ! nvv4l2decoder ! queue ! nv3dsink sync=false

.PHONY: install-basic
install-basic:
	sudo apt install -y v4l-utils gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev mesa-utils

.PHONY: install-libuvc-theta
install-libuvc-theta:
	echo "Installing libuvc-theta"
	sudo apt install -y libjpeg-dev cmake
	mkdir -p $(LIBUVC_THETA_BUILD_DIR) && $(CMAKE) -S $(LIBUVC_THETA_DIR) -B $(LIBUVC_THETA_BUILD_DIR) && $(MAKE) -C $(LIBUVC_THETA_BUILD_DIR)
	sudo $(MAKE) -C $(LIBUVC_THETA_BUILD_DIR) install

.PHONY: install-libuvc-theta-sample
install-libuvc-theta-sample:
	echo "Installing libuvc-theta-sample"
	$(MAKE) -C $(LIBUVC_THETA_SAMPLE_DIR)

.PHONY: install-v4l2loopback
install-v4l2loopback:
	echo "Installing v4l2loopback"
	$(MAKE) -C $(V4L2LOOPBACK_DIR) && sudo $(MAKE) -C $(V4L2LOOPBACK_DIR) install
	sudo depmod -a

.PHONY: install-gstthetauvc
install-gstthetauvc:
	echo "Installing gstthetauvc"
	$(MAKE) -C $(GSTTHETAUVC_DIR)
	sudo cp $(GSTTHETAUVC_DIR)/gstthetauvc.so /usr/lib/aarch64-linux-gnu/gstreamer-1.0/

.PHONY: install-opencv
install-opencv:
	sudo apt install -y python3 python3-dev python3-numpy python3-pip libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad cmake gcc g++ libavcodec-dev libavformat-dev libswscale-dev libgtk-3-dev
	$(CMAKE) -S $(OPENCV_DIR) -B $(OPENCV_DIR)/build -D CMAKE_BUILD_TYPE=RELEASE -D OPENCV_ENABLE_NONFREE=ON  -D WITH_GSTREAMER=ON -D WITH_LIBV4L=ON
	$(MAKE) -C $(OPENCV_DIR)/build
	sudo $(MAKE) -C $(OPENCV_DIR)/build install

.PHONY: python
python:
	PYTHONPATH=/usr/local/lib/python3.8/site-packages:$PYTHONPATH python3 $(PWD)/ml/main.py
	# FIXME That PYTHONPATH is temprary solution. It should be fixed.

clean:
	rm -rf $(LIBUVC_THETA_BUILD_DIR)
