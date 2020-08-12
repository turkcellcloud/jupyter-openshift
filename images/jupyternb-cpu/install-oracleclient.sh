#!/bin/bash

set -x
set -eo pipefail

echo '########## Installing Oracle Client 12.2.0.1 ###########'
yum -y install /tmp/src/oracle/libaio-0.3.109-13.el7.x86_64.rpm
yum -y install /tmp/src/oracle/oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
yum clean all
rm -f /tmp/src/oracle/*.rpm

echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient12.2.conf
ldconfig
export PATH=$PATH:/usr/lib/oracle/12.2/client64/bin

