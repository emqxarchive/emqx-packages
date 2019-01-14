# Keep this short to avoid bloating beam files with long file path info
TOPDIR := /tmp/emqx
SRCDIR := $(TOPDIR)/$(PKG_VSN)
BUILT := $(SRCDIR)/BUILT
dash := -
none :=
space := $(none) $(none)
RPM_VSN ?= $(shell echo $(PKG_VSN) | grep -oE "[0-9]+\.[0-9]+(\.[0-9]+)?")
RPM_REL ?= $(shell echo $(PKG_VSN) | grep -oE "(alpha|beta|rc)\.[0-9]")

ifndef OSTYPE
	OSTYPE := $(none)
else
	OSTYPE := -$(OSTYPE)
endif

TARGET_PKG := ${EMQX_NAME}$(OSTYPE)-v$(RPM_VSN)-$(RPM_REL).x86_64
ifeq ($(RPM_REL),)
	# no tail
	RPM_REL := 1
	TARGET_PKG := ${EMQX_NAME}$(OSTYPE)-v$(RPM_VSN).x86_64
endif
SOURCE_PKG := emqx$(OSTYPE)-v$(RPM_VSN)-$(RPM_REL).x86_64

SYSTEMD := $(shell if command -v systemctl >/dev/null 2>&1; then echo yes; fi)
# Not $(PWD) as it does not work for make -C
CURDIR := $(shell pwd)

SERVICE_SRC := $(if $(SYSTEMD),$(CURDIR)/emqx.service,$(CURDIR)/init.script)
SERVICE_DST := $(if $(SYSTEMD),%{_unitdir}/emqx.service,%{_initddir}/emqx)

POST_ADDITION := $(if $(SYSTEMD),%systemd_post %{_name}.service,echo post)
PREUN_ADDITION := $(if $(SYSTEMD),%systemd_preun %{_name}.service,echo preun)

.PHONY: all
all: | $(BUILT)
	rpmbuild -v -bb \
		--define "_name emqx" \
		--define "_topdir $(TOPDIR)" \
		--define "_version $(RPM_VSN)" \
		--define "_reldir $(SRCDIR)/_rel/emqx" \
		--define "_release $(RPM_REL)" \
		--define "_service_src $(SERVICE_SRC)" \
		--define "_service_dst $(SERVICE_DST)" \
		--define "_post_addition $(POST_ADDITION)" \
		--define "_preun_addition $(PREUN_ADDITION)" \
		--define "_ostype $(OSTYPE)" \
		emqx.spec
	mkdir -p $(CURDIR)/../package
	cp $(TOPDIR)/RPMS/x86_64/$(SOURCE_PKG).rpm $(CURDIR)/../package/$(TARGET_PKG).rpm

$(BUILT):
	mkdir -p $(TOPDIR)
	if [ ! -d $(SRCDIR) ]; then git clone -b $(REL_TAG) https://github.com/emqx/emqx-rel $(SRCDIR); fi
	cd $(SRCDIR) && make && mkdir BUILT

clean:
	rm -rf $(SRCDIR)

