# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib,urllib2
import re
import hashlib

class Vuln(ABVuln):
    poc_id = 'c353b116-b1be-455b-800c-29f697cdfaca'
    name = 'DTCMS /scripts/swfupload/swfupload.swf 跨站脚本' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-10-26'  # 漏洞公布时间
    desc = '''
        动力启航DTCMS网站管理系统 3.0 /scripts/swfupload/swfupload.swf文件存在FlashXss漏洞。
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=069817
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'DTCMS'  # 漏洞应用名称
    product_version = '3.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ea51b080-b746-491f-94c9-292b457c1bd8'
    author = '国光'  # POC编写者
    create_date = '2018-05-10' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            flash_md5 = "3a1c6cc728dddc258091a601f28a9c12"
            payload = "/scripts/swfupload/swfupload.swf"
            verify_url = '{target}'.format(target=self.target)+payload
            request = urllib2.Request(verify_url)
            response = urllib2.urlopen(request)
            content = response.read()
            md5_value = hashlib.md5(content).hexdigest()
            if md5_value in flash_md5:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))


    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()