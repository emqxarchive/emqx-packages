deb: clean package

prepare:
	mkdir -p emqx-$(PKG_VSN)
	git clone -b $(REL_TAG) https://github.com/emqx/emqx-rel emqx-$(PKG_VSN)
	cp debian -r emqx-$(PKG_VSN)/
	cd emqx-$(PKG_VSN) && dpkg-buildpackage -us -uc && rm -rf ../debian && mv debian/ ../

package: prepare
	mkdir -p ../package
	cp emqx_$(PKG_VSN)_*.deb ../package
	rm -rf emqx*
clean:
	rm -rf emqx*
