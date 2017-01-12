emq-package
===========

EMQ RPM/Debian Packages
NOTICE: Requires Erlang/OTP R18+ to build.

Build on Linux Debian/Ubuntu
----------------------------

```

make
sudo dpkg -i emqttd_${EMQ_VERSION}_amd64.deb

```

Build on Linux Centos/Redhat
----------------------------

```
yum install rpm-build
make
sudo rpm -ivh  —force emqttd-${EMQ_VERSION}-1.el7.centos.x86_64.rpm

```

License
-------

Apache License Version 2.0