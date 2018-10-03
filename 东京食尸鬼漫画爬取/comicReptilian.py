# -*- coding: utf-8 -*-
import requests
import traceback
import re
import os
import chardet
baseUrl='http://comic.kukudm.com'
baseImgUrl='http://n5.1whour.com/'


mainUrl='http://comic.kukudm.com/comiclist/1393/index.htm'


def getHTMLText(url):               #根据url获得当前的文本信息
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()        #用于抛出异常
        #r.encoding=r.apparent_encoding#调整编码格式 原本这里apparent_encoding是错的 GB2312 实际网页中显示是GBK
        r.encoding="gbk"
        return r.text               #返回文本信息
    except:
        traceback.print_exc()       #显示异常
        return "Error"
    
def findPages(url):
    html=getHTMLText(url)
    url_lt=re.findall(r'共\d{2}页',html)
    num=(url_lt[0].split("共")[1]).split("页")[0]
    return num
    
def findImgUrl(url):
    html=getHTMLText(url)
    url_lt=re.findall(r'<IMG SRC=\'\".*?\.jpg',html)
    resultUrl=baseImgUrl+url_lt[0].split("\"")[2]
    return resultUrl
    
    
def downloadPic(url,path,num):
    root="D://comic//"
    root=root+path
    if not os.path.exists(root):    #如果根目录不存在，就自己设一个根目录
        os.mkdir(root)
    r=requests.get(url)    
    path=root+str(num)+".jpg"  #生成该图片的存储路径
    r=requests.get(url)
    with open(path,'wb') as f:
        f.write(r.content)
        f.close()
        print("文件保存成功")
    
#匹配的格式如下
#<A href='/comiclist/1393/26070/1.htm' target='_blank'>东京食尸鬼 1话</A>
#num表示画数 有RE 1至178话 以及RE 最终话   以及普通1至143画
def parsePage(html,num,RE):  #根据网站的文本信息，匹配合适的正则表达式存入列表 理论上只有一个
    try:
        if RE!="":
            middle=RE+" "+str(num)
        else:
            middle=str(num)      
        url_lt=re.findall(r'<A href=["\']/comiclist/1393/\d{5}/1.htm\' target=\'_blank\'>东京食尸鬼 '+middle+r'话</A>',html)
        #url_lt=re.findall(r'<A href=["\']/comiclist/1393/\d{5}/1.htm\' target=\'_blank\'>东京食尸鬼 RE 最终话</A>',html)
        url=(url_lt[0].split("href=\'")[1]).split("1.htm\'")[0]
        url=baseUrl+url
        firstUrl=url+"1.htm"
        pages=findPages(firstUrl)
        print(pages)
        for i in range(int(pages)):
            thisUrl=url+str(i+1)+".htm"
            thisImgUrl=findImgUrl(thisUrl)
            downloadPic(thisImgUrl,RE+str(num)+"//",i+1)
                    
    except:                                     #异常处理
        print("Something Wrong in ParsePage") 
        traceback.print_exc()                   #打印异常




def main():
    html=getHTMLText(mainUrl)
    parsePage(html,"最终","RE")
    
main()