# -*- coding: utf8 -*-
import re,os,sys,json


import os
os.remove(__file__)#自毁

if os.path.exists('/etc/openvpn/VPNmod/')==False:#VPNmod目录不存在
  os.makedirs('/etc/openvpn/VPNmod/')


os.chdir("/etc/openvpn/VPNmod/")#切换工作路径


def GetInput(Info,Type="str"):
  print Info
  Input=raw_input("--> ")
  if Input=="" and Type!="Default":
    print "this is required!"
    return GetInput(Info,Type)
  if Type=="int":#整型
    try:
      int(Input)
    except ValueError:#数值错误
      print "only input num"
      return GetInput(Info,Type)
  return Input

def Get_local_ip():#查询本机IP
 import socket
 try:
  csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  csock.connect(('8.8.8.8', 80))
  (addr, port) = csock.getsockname()
  csock.close()
  return addr
 except socket.error:
  return "127.0.0.1"

def CheckDNS(dns):#检查DNS
  reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
  if reip.search(dns)==None:#正则匹配~最小6字符，最大16字符且为英文
    print "DNS服务器格式错误，必须为IP地址！\n\n"
    DNS=GetInput("输入DNS服务器地址，为空则使用114.114.114.144","Default")
    if DNS=="":
      DNS="114.114.114.144"
      return DNS
    CheckDNS(DNS)
    
  return dns
  
  
path="/etc/openvpn/"#对接文件保存地址通常为openvpn目录

if raw_input("Input\"n\"to exit,or press any key to continue -> ")=="n":
  print "canceled~"
  sys.exit(0)

print 
if os.path.exists("%sserver.conf"%path)==False:
  print "can't find openvpn conf，please confirm openvpn install status！"
  sys.exit(0)

'''
if os.path.exists("Auth.py"):
  os.remove("Auth.py")
  
if os.path.exists("Auth.sh"):
  os.remove("Auth.sh")
  
if os.path.exists("disconnect.py"):
  os.remove("disconnect.py")
  
if os.path.exists("disconnect.sh"):
  os.remove("disconnect.sh")
'''

print "[VPNmod] Set ServerInfo"
while 1:
  IP=Get_local_ip()
  Dict={"Url":"","ServerCode":""}
  Dict["Url"]=GetInput("WebManagement Domain Example:xxx.com(only domain,don't contain http://)")
  Dict["ServerCode"]=GetInput("ServerCode: ")
  print "[ServerInfo]\nWebManagement Domain： %s\nServerCode： %s\nServerIP： %s"%(Dict["Url"],Dict["ServerCode"],IP )
  if raw_input("Input 'r' to reinput or press any key to continue")!="r":
    break

open("%sconfig.json"%path,"w").write(json.dumps(Dict))

print "[VPNmod] Modify openvpn conf"
  
fp=open("%sserver.conf"%path,"r")
conf=fp.read()
Lines=conf.split("\n")
confs=[i for i in Lines if "client-connect" not in i and "client-disconnect" not in i and "auth-user-pass-verify" not in i and "max-clients" not in i and 'push "dhcp-option DNS' not in i and "client-to-client" not in i]
confs.append("auth-user-pass-verify /etc/openvpn/VPNmod/Auth.sh via-env") 
confs.append("client-disconnect /etc/openvpn/VPNmod/disconnect.sh")

print "[VPNmod] Modify openvpn conf->Set the max online users num(required)"

MaxClients=GetInput("Please set the max online users num","int")
confs.append("max-clients %s"%MaxClients)

print

print "max online users num：%s …………OK"%MaxClients

print 

reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

'''
DNS="Default"

if raw_input("是否修改DNS(否则使用默认)？y/n\n--> ")=="y":
  print "[VPNmod] 修改DNS服务器->设置DNS服务器(选填)"
  DNS=GetInput("输入DNS服务器地址，为空则使用182.254.210.152","Default")
  if DNS=="":
    DNS="182.254.210.152"
  else:
    CheckDNS(DNS)
  confs.append('push "dhcp-option DNS %s"'%DNS)
  print "设置DNS服务器：%s…………OK"%DNS
'''

print

'''
if raw_input("开启子网互通？y/n\n--> ")!="n":
  print "允许开启子网互通"
  confs.append('client-to-client')
  print "子网互通…………OK"
'''
print 

ServerConf="\n".join(confs)#生成配置文件
fp=open("%sserver.conf"%path,"w")
fp.write(ServerConf)#写入配置文件
print "Write openvpn server conf…………ok"

print """[Server Info]
WebManagement Domain: %s
Server IP: %s
Server Code: %s
------
please confirm it!!!!

"""%(Dict["Url"],Get_local_ip(),Dict["ServerCode"])

print

'''
print """常用命令提示:
服务器测速: python /etc/openvpn/speedtest.py
常用工具安装命令: yum install screen wget nano
"""
'''
