
FINAL_OUTPUT_DIR=FINAL_RPMS
TARBALL_DIR=dist
TOP_DIR=$(shell pwd)
DEFINES=--define '_topdir $(shell pwd)' --define '_tmppath $(shell pwd)/tmp' --define '_sysconfdir /etc' --define '_localstatedir /var'
rpms:	clean package

prepare:
	mkdir -p BUILD SOURCES SPECS SRPMS RPMS tmp dist emqx-${EMQ_VERSION}
	git clone -b emqx30_package https://github.com/emqx/emqx-rel emqx-${EMQ_VERSION}
	cd emqx-${EMQ_VERSION} && make
	rm -rf emqx-${EMQX_VERSION}/deps/gen_rpc/_build/
	cd ../
	tar -zcf emqx-${EMQ_VERSION}.tar.gz emqx-${EMQ_VERSION}
	cp -R emqx-${EMQ_VERSION} dist
	cp emqx-${EMQ_VERSION}.tar.gz SOURCES
	cp emqx.spec SPECS

package: prepare
	mkdir -p $(FINAL_OUTPUT_DIR)
	rpmbuild -vv -bb --nodeps SPECS/emqx.spec $(DEFINES)
	mkdir ../package

	file=$$(basename RPMS/x86_64/emqx-${EMQ_VERSION}*); \
	extension=$${file##*.};\
	uname=$$(uname -m);\
	cp RPMS/x86_64/$${file} ../package/emqx-3.0.$${uname}.$${extension}
	rm -rf BUILDROOT BUILD SOURCES SPECS SRPMS RPMS tmp $(FINAL_OUTPUT_DIR) dist emqx-${EMQ_VERSION} emqx-${EMQ_VERSION}.tar.gz

clean:
	rm -rf BUILDROOT BUILD SOURCES SPECS SRPMS RPMS tmp $(FINAL_OUTPUT_DIR) dist emqx-${EMQ_VERSION} emqx-${EMQ_VERSION}.tar.gz ../package
