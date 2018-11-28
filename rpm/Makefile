# Keep this short to avoid bloating beam files with long file path info
TOPDIR = /tmp/emqx
SRCDIR = $(TOPDIR)/$(REL_VSN)
BUILT = $(SRCDIR)/BUILT
dash = -
none :=
space := $(none) # eol
RPM_VSN = $(word 1,$(subst $(dash),$(space),$(REL_VSN:v%=%)))
vsn_prefix = v$(RPM_VSN)-
RPM_REL = $(REL_VSN:$(vsn_prefix)%=%)
ifeq ($(RPM_REL),$(REL_VSN))
	# no tail
	RPM_REL = 1
endif

SYSTEMD = $(shell if command -v systemctl >/dev/null 2>&1; then echo yes; fi)

SERVICE_SRC = $(if $(SYSTEMD),$(shell pwd)/emqx.service,$(shell pwd)/init.script)
SERVICE_DST = $(if $(SYSTEMD),%{_unitdir}/emqx.service,%{_initddir}/emqx)

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
		emqx.spec

$(BUILT):
	mkdir -p $(TOPDIR)
	git clone -b $(REL_TAG) https://github.com/emqx/emqx-rel $(SRCDIR)
	cd $(SRCDIR) && VSN=$(REL_VSN) make && mkdir BUILT

