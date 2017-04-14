export

OS            = $(shell uname -s)
EMQ_VERSION   = 2.1.1
##
## Support RPM and Debian based linux systems
##
ifeq ($(OS),Linux)
	ARCH          = $(shell uname -m)
	ISRPM         = $(shell cat /etc/redhat-release 2> /dev/null)
	ISDEB         = $(shell cat /etc/debian_version 2> /dev/null)
	ISSLES        = $(shell cat /etc/SuSE-release 2> /dev/null)
	ifneq ($(ISRPM),)
	OSNAME        = RedHat
	PKGERDIR      = rpm
	BUILDDIR      = rpmbuild
else
	ifneq ($(ISDEB),)
	OSNAME        = Debian
	PKGERDIR      = deb
	BUILDDIR      = debuild
else
	ifneq ($(ISSLES),)
	OSNAME        = SLES
	PKGERDIR      = rpm
	BUILDDIR      = rpmbuild
endif  # SLES
endif  # deb
endif  # rpm
endif  # linux

.PHONY: ostype

## Call platform dependent makefile
ostype: 
	$(if $(PKGERDIR),,$(error "Operating system '$(OS)' not supported by emq_package"))
	cd $(PKGERDIR) && $(MAKE)

clean:
	rm -rf package
