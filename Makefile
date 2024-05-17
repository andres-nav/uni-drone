PWD		:= $(shell pwd)
MAKE		:= /usr/bin/make
CMAKE		:= /usr/bin/cmake
AUTORECONF	:= /usr/bin/autoreconf
LIBUVC_THETA_DIR := $(PWD)/libuvc-theta
LIBUVC_THETA_BUILD_DIR := $(LIBUVC_THETA_DIR)/build
LIBUVC_THETA_SAMPLE_DIR := $(PWD)/libuvc-theta-sample/gst
# V4L2LOOPBACK_DIR := $(PWD)/v4l2loopback
GSTTHETAUVC_DIR := $(PWD)/gstthetauvc/thetauvc

.PHONY: all
all: run

.PHONY: install
install: clean install-basic install-libuvc-theta install-libuvc-theta-sample install-gstthetauvc
	@echo "Installation completed."

.PHONY: viewer
viewer:
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_viewer

.PHONY: loopback
loopback:
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_loopback

.PHONY: gstthetauvc
gstthetauvc:
	LD_LIBRARY_PATH=/usr/local/lib GST_PLUGIN_PATH=$(GSTTHETAUVC_DIR)

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

# .PHONY: install-v4l2loopback
# install-v4l2loopback:
# 	echo "Installing v4l2loopback"
# 	$(MAKE) -C $(V4L2LOOPBACK_DIR) && sudo $(MAKE) -C $(V4L2LOOPBACK_DIR) install && sudo depmod -a
# 	sudo depmod -a

.PHONY: install-gstthetauvc
install-gstthetauvc:
	echo "Installing gstthetauvc"
	$(MAKE) -C $(LIBUVC_THETA_SAMPLE_DIR)

clean:
	rm -rf $(LIBUVC_THETA_BUILD_DIR)
