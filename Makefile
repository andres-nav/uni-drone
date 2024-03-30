PWD		:= $(shell pwd)
MAKE		:= /usr/bin/make
CMAKE		:= /usr/bin/cmake
LIBUVC_THETA_DIR := $(PWD)/libuvc-theta
LIBUVC_THETA_BUILD_DIR := $(LIBUVC_THETA_DIR)/build
LIBUVC_THETA_SAMPLE_DIR := $(PWD)/libuvc-theta-sample/gst
V4L2LOOPBACK_DIR := $(PWD)/v4l2loopback

.PHONY: all clean install run install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback

all: clean install

install: install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback
	@echo "Installation completed."

run:
	@$(LIBUVC_THETA_SAMPLE_DIR)/gst_viewer

install-libuvc-theta:
	echo "Building libuvc-theta"
	mkdir -p $(LIBUVC_THETA_BUILD_DIR) && $(CMAKE) -S $(LIBUVC_THETA_DIR) -B $(LIBUVC_THETA_BUILD_DIR) && $(MAKE) -C $(LIBUVC_THETA_BUILD_DIR)
	sudo $(MAKE) -C $(LIBUVC_THETA_BUILD_DIR) install

install-libuvc-theta-sample:
	echo "Building libuvc-theta-sample"
	$(MAKE) -C $(LIBUVC_THETA_SAMPLE_DIR)

install-v4l2loopback:
	echo "Building v4l2loopback"
	$(MAKE) -C $(V4L2LOOPBACK_DIR) && sudo $(MAKE) -C $(V4L2LOOPBACK_DIR) install && sudo depmod -a

clean:
	rm -rf $(LIBUVC_THETA_BUILD_DIR)
