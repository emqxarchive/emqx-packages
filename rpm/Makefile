
FINAL_OUTPUT_DIR=FINAL_RPMS
TARBALL_DIR=dist
TOP_DIR=$(shell pwd)
DEFINES=--define '_topdir $(shell pwd)' --define '_tmppath $(shell pwd)/tmp' --define '_sysconfdir /etc' --define '_localstatedir /var'
rpms:	clean package

prepare:
	mkdir -p BUILD SOURCES SPECS SRPMS RPMS tmp dist emqx-${EMQX_VERSION}
	git clone -b ${REL_TAG} https://github.com/emqx/emqx-rel emqx-${EMQX_VERSION}
	cd emqx-${EMQX_VERSION} && make
	rm -rf emqx-${EMQX_VERSION}/deps/gen_rpc/_build/
	cd ../
	tar -zcf emqx-${EMQX_VERSION}.tar.gz emqx-${EMQX_VERSION}
	cp -R emqx-${EMQX_VERSION} dist
	cp emqx-${EMQX_VERSION}.tar.gz SOURCES
	cp emqx.spec SPECS

package: prepare
	mkdir -p $(FINAL_OUTPUT_DIR)
	rpmbuild -vv -bb --nodeps SPECS/emqx.spec $(DEFINES)
	mkdir -p ../package
	file=$$(basename RPMS/x86_64/emqx-${EMQX_VERSION}*); \
	extension=$${file##*.};\
	uname=$$(uname -m);\
	cp RPMS/x86_64/$${file} ../package/emqx-$${versionid}.$${uname}.$${extension}
	rm -rf BUILDROOT BUILD SOURCES SPECS SRPMS RPMS tmp $(FINAL_OUTPUT_DIR) dist emqx-${EMQX_VERSION} emqx-${EMQX_VERSION}.tar.gz

clean:
	rm -rf BUILDROOT BUILD SOURCES SPECS SRPMS RPMS tmp $(FINAL_OUTPUT_DIR) dist emqx-${EMQX_VERSION} emqx-${EMQX_VERSION}.tar.gz ../package
