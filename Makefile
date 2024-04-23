PWD		:= $(shell pwd)
MAKE		:= /usr/bin/make
CMAKE		:= /usr/bin/cmake
AUTORECONF	:= /usr/bin/autoreconf
LIBUVC_THETA_DIR := $(PWD)/libuvc-theta
LIBUVC_THETA_BUILD_DIR := $(LIBUVC_THETA_DIR)/build
LIBUVC_THETA_SAMPLE_DIR := $(PWD)/libuvc-theta-sample/gst
# NVIDIA_CODEC_DIR := $(PWD)/nvidia-codec/Samples
# NVIDIA_CODEC_BUILD_DIR := $(NVIDIA_CODEC_DIR)/build
LIBUSB_DIR := $(PWD)/libusb
V4L2LOOPBACK_DIR := $(PWD)/v4l2loopback

.PHONY: all clean install run install-libusb install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback

all: run

install: clean install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback
	@echo "Installation completed."

run:
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_viewer

loopback:
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_loopback

# install-libusb:
# 	echo "Building libusb"
# 	sudo apt install -y automake libudev-dev
# 	$(AUTORECONF) -f -i $(LIBUSB_DIR)
# 	$(LIBUSB_DIR)/configure #--enable-udev --disable-static
# 	make -C $(LIBUSB_DIR) -f Makefile.in
# 	sudo make -C $(LIBUSB_DIR) install


install-libuvc-theta:
	echo "Installing libuvc-theta"
	sudo apt install -y libjpeg-dev cmake
	mkdir -p $(LIBUVC_THETA_BUILD_DIR) && $(CMAKE) -S $(LIBUVC_THETA_DIR) -B $(LIBUVC_THETA_BUILD_DIR) && $(MAKE) -C $(LIBUVC_THETA_BUILD_DIR)
	sudo $(MAKE) -C $(LIBUVC_THETA_BUILD_DIR) install

install-libuvc-theta-sample:
	echo "Installing libuvc-theta-sample"
	sudo apt install -y v4l-utils
	sudo apt install -y gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav
	sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libgstreamer-plugins-base1.0-dev
	sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev
	sudo apt install -y mesa-utils
	$(MAKE) -C $(LIBUVC_THETA_SAMPLE_DIR)

install-v4l2loopback:
	echo "Installing v4l2loopback"
	$(MAKE) -C $(V4L2LOOPBACK_DIR) && sudo $(MAKE) -C $(V4L2LOOPBACK_DIR) install && sudo depmod -a

# install-nvidia-codec:
# 	echo "Installing nvidia codec"
# 	sudo apt install -y cmake build-essential
# 	mkdir -p $(NVIDIA_CODEC_BUILD_DIR) && $(CMAKE) -S $(NVIDIA_CODEC_DIR) -B $(NVIDIA_CODEC_BUILD_DIR) -DCMAKE_BUILD_TYPE=Release && $(MAKE) -C $(NVIDIA_CODEC_BUILD_DIR)
# 	sudo $(MAKE) -C $(NVIDIA_CODEC_BUILD_DIR) install

clean:
	rm -rf $(LIBUVC_THETA_BUILD_DIR)
