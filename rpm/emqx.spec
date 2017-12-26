%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}
Name:    emqx	
Version: 2.4
Release: 1%{?dist}
Summary: emqx
Group:	 System Environment/Daemons
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
mkdir -p %{buildroot}%{_localstatedir}/lib/emqx/emqx/sbin
mkdir -p %{buildroot}%{_localstatedir}/lib/emqx/emqx/etc

install -p -D -m 0755 %{relpath}/bin/emqx %{buildroot}%{_localstatedir}/lib/emqx/emqx/sbin
install -p -D -m 0755 %{relpath}/bin/emqx_ctl %{buildroot}%{_localstatedir}/lib/emqx/emqx/sbin

cp -R %{relpath}/lib           %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib
cp -R %{relpath}/erts-*        %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib
cp -R %{relpath}/releases      %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib

cp %{relpath}/bin/cuttlefish               %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib/bin
cp %{relpath}/bin/install_upgrade_escript  %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib/bin
cp %{relpath}/bin/nodetool                 %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib/bin
cp %{relpath}/bin/start_clean.boot         %{buildroot}%{_localstatedir}/lib/emqx/emqx/lib/bin

cp -R %{relpath}/etc/* %{buildroot}%{_localstatedir}/lib/emqx/emqx/etc

cp -R %{relpath}/data/* %{buildroot}%{_localstatedir}/lib/emqx

command -v service >/dev/null 2>&1 || { install -m755  %{_topdir}/emqx.service %{buildroot}%{_localstatedir}/lib/emqx/emqx/; }
command -v systemctl >/dev/null 2>&1 || { install -m755 %{_topdir}/init.script %{buildroot}%{_localstatedir}/lib/emqx/emqx/; }

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
    mkdir /usr/lib64/emqx
    mkdir /etc/emqx
    \cp -rf /var/lib/emqx/emqx/etc/* /etc/emqx/
    \cp -rf /var/lib/emqx/emqx/sbin/* /usr/sbin/
    \cp -rf /var/lib/emqx/emqx/lib/* /usr/lib64/emqx/

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
        rm -rf /etc/init.d/emqx
    else
        systemctl disable emqx.service
    fi
    rm -rf /etc/emqx/
    rm -rf /usr/lib64/emqx/
    rm -rf /usr/sbin/emqx
    rm -rf /usr/sbin/emqx_ctl

fi
exit 0

%files
%defattr(-,root,root)
/var/ 
%doc

%clean
rm -rf %{buildroot}

%changelog

