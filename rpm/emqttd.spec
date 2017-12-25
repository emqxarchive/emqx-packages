%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}
Name:    emqttd		
Version: 2.3.2
Release: 1%{?dist}
Summary: emqttd
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
%define relpath       %{_builddir}/%{buildsubdir}/_rel/emqttd
%define buildroot_lib %{buildroot}%{_libdir}/emqttd
%define buildroot_etc %{buildroot}%{_sysconfdir}/emqttd
%define buildroot_bin %{buildroot_lib}/bin

mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd
mkdir -p %{buildroot}%{_localstatedir}/log/emqttd
mkdir -p %{buildroot}%{_localstatedir}/run/emqttd
mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib
mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib/bin
mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/sbin
mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/etc

install -p -D -m 0755 %{relpath}/bin/emqttd %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/sbin
install -p -D -m 0755 %{relpath}/bin/emqttd_ctl %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/sbin

cp -R %{relpath}/lib           %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib
cp -R %{relpath}/erts-*        %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib
cp -R %{relpath}/releases      %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib

cp %{relpath}/bin/cuttlefish               %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib/bin
cp %{relpath}/bin/install_upgrade_escript  %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib/bin
cp %{relpath}/bin/nodetool                 %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib/bin
cp %{relpath}/bin/start_clean.boot         %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/lib/bin

cp -R %{relpath}/etc/* %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/etc

cp -R %{relpath}/data/* %{buildroot}%{_localstatedir}/lib/emqttd

command -v service >/dev/null 2>&1 || { install -m755  %{_topdir}/emqttd.service %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/; }
command -v systemctl >/dev/null 2>&1 || { install -m755 %{_topdir}/init.script %{buildroot}%{_localstatedir}/lib/emqttd/emqttd/; }

%pre
# Pre-install script
if ! getent group emqtt >/dev/null 2>&1; then
        groupadd -r emqtt
fi

if getent passwd emqtt >/dev/null 2>&1; then
        usermod -d %{_localstatedir}/lib/emqttd emqtt || true
else
    useradd -r -g emqtt \
           --home %{_localstatedir}/lib/emqttd \
           --comment "emqtt user" \
           --shell /bin/bash \
           emqtt
fi

%post
if [ $1 == 1 ];then
    mkdir /usr/lib64/emqttd
    mkdir /etc/emqttd
    \cp -rf /var/lib/emqttd/emqttd/etc/* /etc/emqttd/
    \cp -rf /var/lib/emqttd/emqttd/sbin/* /usr/sbin/
    \cp -rf /var/lib/emqttd/emqttd/lib/* /usr/lib64/emqttd/

    if [ -e /var/lib/emqttd/emqttd/init.script ] ; then
        \cp -rf /var/lib/emqttd/emqttd/init.script /etc/init.d/emqttd
        chown root:root /etc/init.d/emqttd
        sbin/chkconfig --add emqttd
    else
        \cp -rf /var/lib/emqttd/emqttd/emqttd.service /usr/lib/systemd/system/emqttd.service
        systemctl enable emqttd.service
    fi
    chown -R emqtt:emqtt /var/log/emqttd/
    chown -R emqtt:emqtt /var/lib/emqttd/
fi


%preun
# Pre-uninstall script

# Only on uninstall, not upgrades
if [ "$1" = 0 ] ; then
    if [ -e /etc/init.d/emqttd ] ; then
        /sbin/service emqttd stop > /dev/null 2>&1
        /sbin/chkconfig --del emqttd
        rm -rf /etc/init.d/emqttd
    else
        systemctl disable emqttd.service
    fi
    rm -rf /etc/emqttd/
    rm -rf /usr/lib64/emqttd/
    rm -rf /usr/sbin/emqttd
    rm -rf /usr/sbin/emqttd_ctl

fi
exit 0

%files
%defattr(-,root,root)
/var/ 
%doc

%clean
rm -rf %{buildroot}

%changelog

