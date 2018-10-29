deb: clean package

prepare:
	mkdir -p emqx-${EMQX_VERSION}
	git clone -b ${REL_TAG} https://github.com/emqx/emqx-rel emqx-${EMQX_VERSION}
	cp debian -r emqx-${EMQX_VERSION}/
	cd emqx-${EMQX_VERSION} && dpkg-buildpackage -us -uc && rm -rf ../debian && mv debian/ ../

package: prepare
	mkdir -p ../package
	cp emqx_${EMQX_VERSION}_*.deb ../package
	rm -rf emqx*
clean:
	rm -rf emqx*
