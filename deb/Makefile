deb: clean package

prepare:
	mkdir -p emqx-${EMQ_VERSION}
	git clone -b emqx30_package https://github.com/emqtt/emq-relx.git emqx-${EMQ_VERSION}
	cp debian -r emqx-${EMQ_VERSION}/
	cd emqx-${EMQ_VERSION} && dpkg-buildpackage -us -uc && rm -rf ../debian && mv debian/ ../

package: prepare
	mkdir ../package
	cp emqx_${EMQ_VERSION}_*.deb ../package
	rm -rf emqx*
clean:
	rm -rf emqx*
