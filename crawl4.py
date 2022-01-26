'''
Created on 2021年11月9日

@author: Administrator
'''
 
 # -*- coding:UTF-8 -*-
import pandas as pd
import http.client
import os 
#import httplib2
from bs4 import BeautifulSoup
import requests
import time
import datetime
import random 
from multiprocessing.pool import Pool

from url3 import url2
aa=url2()
def get_webservertime(host):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    print(ltime)
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    print(ttime)
    dat="date %u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="time %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    #print (dat,tm)
    #os.system(dat)
    #os.system(tm)
    return ttime.tm_year,ttime.tm_mon,ttime.tm_mday,ttime.tm_hour,ttime.tm_min,ttime.tm_sec
     

 
def getresut3(domainlist,filename, headers,proxyHost ,proxyPort,proxyUser,proxyPass,timeout):
    


    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host" : proxyHost,
        "port" : proxyPort,
        "user" : proxyUser,
        "pass" : proxyPass,
    }

    # 设置 http和https访问都是用HTTP代理
    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    saveone=[]
    for domain in domainlist:
        #url = aa.url+domain
        try:
        #url = 'http://www.shuaia.net/index.html'
#             headers = {
#                     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#             }
             
            html=aa.get(domain,proxies,headers,timeout)
            bf = BeautifulSoup(html, 'lxml')
            targets_url=bf.select("div.ztInfo p")
            #targets_url = bf.find_all(class_='ztInfo')
             
             
            print(targets_url)
            list_url = []
            for each in targets_url:
                list_url.append(each.string)
                #print(html)
            
            targets_url=bf.select("div.siteInfo p")
            for each in targets_url:
                list_url.append(each.string)
            print(list_url)
            if(len(list_url)<8):
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                list_url.append(None)
                
            list_url.append(domain)
            dt=datetime.datetime.now()
            dtstr=dt.strftime('%m/%d/%Y %H:%M:%S %p')
            list_url.append(dtstr)
            saveone.append(list_url)
            #df = pd.DataFrame([list_url])
            #df.to_csv(filename, mode='a', header=None, index=None,encoding='gbk')
            print([list_url])
            #return list_url 
        except Exception as e:
            print("time out")
            return None
    df = pd.DataFrame(saveone)
    df.to_csv(filename, mode='a', header=None, index=None,encoding='gbk')
# #将html保存到文件
# with open('test.txt', 'w') as f:
#     f.write(list_url)
if __name__ == '__main__':
    
    proxy=[]   
    with open("proxy.txt", "r") as f:  # 打开文件
        data = f.read()  # 读取文件
        print(data)
        proxy.append(data)
    name=['备案/许可证号','审核通过日期','主办单位名称','主办单位性质','网站名称','网站备案/许可证号','网站首页地址','网站域名','网站前置审批项','查询域名','查询时间']
    test=pd.DataFrame(columns=name)
    filename='data7.csv'
    test.to_csv(filename,  index=None,encoding='gbk')
    f = open("1406.txt")             # 返回一个文件对象
    line = f.readline()    
    
    # 调用文件的 readline()方法
    domainlist=[]
    pool = Pool(processes=5)
    while line:
        break
        domainlist.append(line.replace('\n', '').replace('\r', ''))  
        #print (line)
        #result=getresut(line)
        if line:
            line = f.readline()  
    
    for i in range(0,len(domainlist),10):
        b=domainlist[i:i+10]
        print (b)
        #u7525.5.tp.16yun.cn 6445 16NETSRM 654404
        #continue
        


    #  设置IP切换头
        tunnel = random.randint(1,10000)
        #headers = {"Proxy-Tunnel": str(tunnel)}
        headers = {
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 "+str(tunnel)
            }
        #getresut2(b,filename, proxies , headers )
        pool.apply_async(getresut3, (b,filename,  headers, proxy[0],proxy[1],proxy[2],proxy[3],10))# 写文件还有点问题
        time.sleep(0.5)
         
    
    pool.close()
    pool.join()
 

    
    