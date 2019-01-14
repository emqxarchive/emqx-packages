# Keep this short to avoid bloating beam files with long file path info
TOPDIR := /tmp/emqx
SRCDIR := $(TOPDIR)/$(PKG_VSN)
BUILT := $(SRCDIR)/BUILT
DEB_VSN := $(PKG_VSN:v%=%)

ifndef ostype
	OSTYPE := $(none)
else
	OSTYPE := -$(ostype)
endif

ARCH := $(shell dpkg --print-architecture)
SOURCE_PKG := emqx_$(DEB_VSN)_$(ARCH)
TARGET_PKG := ${EMQX_NAME}$(OSTYPE)-$(PKG_VSN)_$(ARCH)

.PHONY: all
all: | $(BUILT)
	cp -r debian $(SRCDIR)/
	sed -i "s#<DATETIME>#$(shell date -u '+%a, %d %b %Y %T %z')#g" $(SRCDIR)/debian/changelog
	sed -i "s#<VERSION>#$(DEB_VSN)#g" $(SRCDIR)/debian/changelog
	cd $(SRCDIR) && dpkg-buildpackage -us -uc
	mkdir -p ../package
	cp $(SRCDIR)/../$(SOURCE_PKG).deb ../package/$(TARGET_PKG).deb

$(BUILT):
	mkdir -p $(TOPDIR)
	if [ ! -d $(SRCDIR) ]; then git clone -b $(REL_TAG) https://github.com/emqx/emqx-rel $(SRCDIR); fi
	cd $(SRCDIR) && make && mkdir BUILT

clean:
	rm -rf $(SRCDIR)

