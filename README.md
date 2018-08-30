emqx-packages
=============

EMQ X RPM/Debian Packages

NOTICE: Requires Erlang/OTP R21+ to build since 3.0 release.

Build on Linux Debian/Ubuntu
----------------------------

```

make
sudo dpkg -i emqx_${EMQX_VERSION}_amd64.deb

```

Build on Linux Centos/Redhat
----------------------------

```
yum install rpm-build
make
sudo rpm -ivh —force emqx-${EMQX_VERSION}-1.el7.centos.x86_64.rpm

```

License
-------

Apache License Version 2.0

Author
------

EMQ X Team.
