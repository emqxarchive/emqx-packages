# Keep this short to avoid bloating beam files with long file path info
TOPDIR := /tmp/emqx
SRCDIR := $(TOPDIR)/$(PKG_VSN)
BUILT := $(SRCDIR)/BUILT
DEB_VSN := $(PKG_VSN:v%=%)

ifndef SYSTEM
	SYSTEM := $(none)
else
	SYSTEM := -$(SYSTEM)
endif

ARCH := $(shell dpkg --print-architecture)
SOURCE_PKG := $(EMQX_NAME)_$(DEB_VSN)_$(ARCH)
TARGET_PKG := $(EMQX_NAME)$(SYSTEM)-$(PKG_VSN)_$(ARCH)

.PHONY: all
all: | $(BUILT)
	cp -r debian $(SRCDIR)/
	sed -i "s#<DATETIME>#$(shell date -u '+%a, %d %b %Y %T %z')#g" $(SRCDIR)/debian/changelog
	sed -i "s#<VERSION>#$(DEB_VSN)#g" $(SRCDIR)/debian/changelog
	if [ ! -z $(shell echo $(EMQX_NAME) |grep edge) ]; then \
		sed -i "s/emqx_pkg/emqx_edge_pkg/g" $(SRCDIR)/debian/rules; \
		sed -i "s debian/emqx debian/emqx-edge g" $(SRCDIR)/debian/rules; \
		sed -i "s/Package: emqx/Package: emqx-edge/1" $(SRCDIR)/debian/control; \
	fi
	cd $(SRCDIR) && dpkg-buildpackage -us -uc
	mkdir -p ../package
	cp $(SRCDIR)/../$(SOURCE_PKG).deb ../package/$(TARGET_PKG).deb

$(BUILT):
	mkdir -p $(TOPDIR)
	if [ ! -z $(EMQX_REL) ] && [ -d $(EMQX_REL) ]; then mkdir $(SRCDIR) && cp -r $(EMQX_REL)/. $(SRCDIR); fi
	if [ ! -d $(SRCDIR) ]; then git clone -b $(REL_TAG) https://github.com/emqx/emqx-rel $(SRCDIR); fi
	# cd $(SRCDIR) && make distclean && make $(EMQX_NAME)_pkg && mkdir BUILT

clean:
	rm -rf $(SRCDIR)

