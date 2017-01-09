%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}
Name:    emqttd		
Version: 2.0.6	
Release: 1%{?dist}
Summary: emqttd	
Group:	 System Environment/Daemons
License: Apache License Version 2.0
URL:	 http://www.emqtt.io
Source0:	%{name}-%{version}.tar.gz
BuildRoot:  %_topdir/BUILDROOT
#BuildRequires: gcc,make	
#Requires:	pcre,pcre-devel,openssl,chkconfig

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

mkdir -p %{buildroot_etc}
mkdir -p %{buildroot_lib}
mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd
mkdir -p %{buildroot}%{_localstatedir}/log/emqttd
mkdir -p %{buildroot}%{_localstatedir}/run/emqttd

mkdir -p %{buildroot}/usr/sbin/

cp -r %{relpath}/bin/* %{buildroot}/usr/sbin

cp -R %{relpath}/lib       %{buildroot_lib}
cp -R %{relpath}/erts-*    %{buildroot_lib}
cp -R %{relpath}/releases  %{buildroot_lib}

cp -R %{relpath}/etc/* %{buildroot_etc}

mkdir -p %{buildroot}%{_localstatedir}/lib/emqttd

cp -R %{relpath}/data/* %{buildroot}%{_localstatedir}/lib/emqttd

mkdir -p %{buildroot}%{_sysconfdir}/init.d

#install -m755 %{_topdir}/init.script  %{buildroot}%{_sysconfdir}/init.d/emqttd

%post 
if [ $1 == 1 ];then 
	/sbin/chkconfig --add emqttd 
fi 

%files
%defattr (-,root,root,0755)
/etc/ 
/usr/ 
/var/ 
%doc

%clean
rm -rf %{buildroot}

%changelog

