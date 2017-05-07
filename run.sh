#!/bin/sh
#rpm -ivh http://mirrors.sohu.com/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm
yum install -y openvpn unzip nano

get_char() 
{ 
    SAVEDSTTY=`stty -g` 
    stty -echo 
    stty cbreak 
    dd if=/dev/tty bs=1 count=1 2> /dev/null 
    stty -raw 
    stty echo 
    stty $SAVEDSTTY 
} 
 
echo "Press any key to continue!" 
char=`get_char` 

echo "Set iptables and firewall rules."
iptables -F >/dev/null 2>&1
service iptables save >/dev/null 2>&1
service iptables restart >/dev/null 2>&1
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 3389 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 3306 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 8080 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 8888 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 9999 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 1194 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 60880 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 3399 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 80 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 443 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 440 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 138 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 137 -j ACCEPT >/dev/null 2>&1
iptables -A INPUT -p TCP --dport 22 -j ACCEPT >/dev/null 2>&1
iptables -t nat -A POSTROUTING -j MASQUERADE >/dev/null 2>&1
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT >/dev/null 2>&1


sed -i '/net.ipv4.ip_forward/s/0/1/g' /etc/sysctl.conf 
sysctl -w net.ipv4.ip_forward=1

service iptables save
service iptables restart

chkconfig iptables on
setenforce 0

#wget http://yd.nn920.cn/static/op.zip
echo "DownLoad openvpn server data..."
cd /etc/openvpn
wget http://o9zp7n8q3.bkt.clouddn.com/openvpn-Centos.zip -P /etc/openvpn/ && unzip /etc/openvpn/openvpn-Centos.zip
wget https://raw.githubusercontent.com/LunacyZeus/openvpn-installer-for-Centos-6/master/Start.py && python Start.py
#阿里云DNS
#100.100.2.138
#100.100.2.136

#60.191.134.196
