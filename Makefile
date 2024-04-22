PWD		:= $(shell pwd)
MAKE		:= /usr/bin/make
CMAKE		:= /usr/bin/cmake
AUTORECONF	:= /usr/bin/autoreconf
LIBUVC_THETA_DIR := $(PWD)/libuvc-theta
LIBUVC_THETA_BUILD_DIR := $(LIBUVC_THETA_DIR)/build
LIBUVC_THETA_SAMPLE_DIR := $(PWD)/libuvc-theta-sample/gst
LIBUSB_DIR := $(PWD)/libusb
V4L2LOOPBACK_DIR := $(PWD)/v4l2loopback

.PHONY: all clean install run install-libusb install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback

all: clean install

install: install-libuvc-theta install-libuvc-theta-sample install-v4l2loopback
	@echo "Installation completed."

run:
	LD_LIBRARY_PATH=/usr/local/lib $(LIBUVC_THETA_SAMPLE_DIR)/gst_viewer

# install-libusb:
# 	echo "Building libusb"
# 	sudo apt install -y automake libudev-dev
# 	$(AUTORECONF) -f -i $(LIBUSB_DIR)
# 	$(LIBUSB_DIR)/configure #--enable-udev --disable-static
# 	make -C $(LIBUSB_DIR) -f Makefile.in
# 	sudo make -C $(LIBUSB_DIR) install


install-libuvc-theta:
	echo "Building libuvc-theta"
	sudo apt install -y cmake
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
