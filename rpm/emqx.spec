%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}
Name:    emqx
Version: 3.0
Release: 1%{?dist}
Summary: emqx
Group:   System Environment/Daemons
License: Apache License Version 2.0
URL:     http://www.emqtt.io
Source0:    %{name}-%{version}.tar.gz
BuildRoot:  %_topdir/BUILDROOT
#BuildRequires: gcc,make
#Requires:  pcre,pcre-devel,openssl,chkconfig

%description
(Erlang MQTT Broker) is a distributed, massively scalable, highly extensible MQTT message broker written in Erlang/OTP.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
#make install DESTDIR=%{buildroot}
%define relpath       %{_builddir}/%{buildsubdir}/_rel/emqx
%define buildroot_lib %{buildroot}%{_libdir}/emqx
%define buildroot_etc %{buildroot}%{_sysconfdir}/emqx
%define buildroot_bin %{buildroot_lib}/bin

mkdir -p %{buildroot}%{_localstatedir}/lib/emqx
mkdir -p %{buildroot}%{_localstatedir}/log/emqx
mkdir -p %{buildroot}%{_localstatedir}/run/emqx
mkdir -p %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib
mkdir -p %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib/bin
mkdir -p %{buildroot}%{_localstatedir}/lib/emqx/emqx/etc

cp -R %{relpath}/lib      %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib
cp -R %{relpath}/erts-*   %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib
cp -R %{relpath}/releases %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib

cp %{relpath}/bin/*       %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib/bin

cp -R %{relpath}/etc/*    %{buildroot}%{_localstatedir}/lib/emqx/emqx/etc

cp -R %{relpath}/data/*   %{buildroot}%{_localstatedir}/lib/emqx

if command -v systemctl >/dev/null 2>&1; then
    install -m755  %{_topdir}/emqx.service %{buildroot}%{_localstatedir}/lib/emqx/emqx/
else
    install -m755 %{_topdir}/init.script %{buildroot}%{_localstatedir}/lib/emqx/emqx/
fi

%pre
# Pre-install script
if ! getent group emqx >/dev/null 2>&1; then
        groupadd -r emqx
fi

if getent passwd emqx >/dev/null 2>&1; then
        usermod -d %{_localstatedir}/lib/emqx emqx || true
else
    useradd -r -g emqx \
           --home %{_localstatedir}/lib/emqx \
           --comment "emqx user" \
           --shell /bin/bash \
           emqx
fi

%post
if [ $1 == 1 ];then
    mkdir /usr/lib/emqx
    mkdir /etc/emqx
    \cp -rf /var/lib/emqx/emqx/etc/* /etc/emqx/
    \cp -rf /var/lib/emqx/emqx/lib/* /usr/lib/emqx/
    ln -s /usr/lib/emqx/bin/emqx /usr/bin/emqx
    ln -s /usr/lib/emqx/bin/emqx_ctl /usr/bin/emqx_ctl

    if [ -e /var/lib/emqx/emqx/init.script ] ; then
        \cp -rf /var/lib/emqx/emqx/init.script /etc/init.d/emqx
        chown root:root /etc/init.d/emqx
        sbin/chkconfig --add emqx
    else
        \cp -rf /var/lib/emqx/emqx/emqx.service /usr/lib/systemd/system/emqx.service
        systemctl enable emqx.service
    fi
    chown -R emqx:emqx /var/log/emqx/
    chown -R emqx:emqx /var/lib/emqx/
fi


%preun
# Pre-uninstall script

# Only on uninstall, not upgrades
if [ "$1" = 0 ] ; then
    if [ -e /etc/init.d/emqx ] ; then
        /sbin/service emqx stop > /dev/null 2>&1
        /sbin/chkconfig --del emqx
        rm -f /etc/init.d/emqx
    else
        systemctl disable emqx.service
        rm -f /usr/lib/systemd/system/emqx.service
    fi
    rm -rf /usr/lib/emqx/
    rm -f /usr/bin/emqx
    rm -f /usr/bin/emqx_ctl

fi
exit 0

%files
%defattr(-,root,root)
/var/ 
%doc

%clean
rm -rf %{buildroot}

%changelog

