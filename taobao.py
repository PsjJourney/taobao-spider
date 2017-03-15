#encoding=utf8  
import re
import requests
import time
import json
limit=4 #爬10页数据，每页44个记录
keystr="iphone7" #搜索关键词
url = 'https://s.taobao.com/search'
rateUrl = 'https://rate.taobao.com/feedRateList.htm'
tmrateUrl = 'https://rate.tmall.com/listTagClouds.htm'
payload = {'q': keystr,'s': '1','ie':'utf8'}  #字典传递url参数，第二字段写要搜索的关键词
rateload = {'auctionNumId': '44404493527','userNumId': '839556000','currentPageNum':'1','pageSize':'20','rateType':'1','folded':'0','ie':'utf8'}  #字典传递url参数
tmrateload = {'itemId': '44404493527','isAll': 'true','isInner':'true','ie':'utf8'}  #字典传递url参数    
file = open('taobao_iphone7.txt','w',encoding='utf-8') #可以指定文件名
print ("本次爬数据开始，搜索关键词为："+keystr+" , 总共要爬的记录"+str(limit*44)+"个，本单实例开始时间： "+str(time.time()))
for k in range(0,limit):        #100次，就是100个页的商品数据
    payload ['s'] = 44*k+1   #此处改变的url参数为s，s为1时第一页，s为45是第二页，89时第三页以此类推                          
    resp = requests.get(url, params = payload)
    #print(resp.url)          #打印访问的网址
    resp.encoding = 'utf-8'  #设置编码
    title = re.findall(r'"raw_title":"([^"]+)"',resp.text,re.I)  #正则保存所有raw_title的内容，这个是书名，下面是价格，地址
    price = re.findall(r'"view_price":"([^"]+)"',resp.text,re.I)    
    loc = re.findall(r'"item_loc":"([^"]+)"',resp.text,re.I)
    sales = re.findall(r'"view_sales":"([^"]+)"',resp.text,re.I)
    pid = re.findall(r'"nid":"([^"]+)"',resp.text,re.I)
    x = len(title)           #每一页商品的数量
    for i in range(0,x) :    #把列表的数据保存到文件中
        # haoping
        rateload ['auctionNumId'] = pid[i]
        rateload ['rateType'] = 1
        respRate = requests.get(rateUrl, params = rateload)
        respRate.encoding = 'utf-8'  #设置编码
        ratevalue = re.findall(r'"total":([^,]+)',respRate.text,re.I)
        pomax = re.findall(r'"maxPage":([^,]+)',respRate.text,re.I)
        positive=ratevalue[0]
        rateload ['rateType'] = 0
        respRate = requests.get(rateUrl, params = rateload)
        respRate.encoding = 'utf-8'  #设置编码
        ratevalue = re.findall(r'"total":([^,]+)',respRate.text,re.I)
        normax = re.findall(r'"maxPage":([^,]+)',respRate.text,re.I)
        middle=ratevalue[0]
        rateload ['rateType'] = -1
        respRate = requests.get(rateUrl, params = rateload)
        respRate.encoding = 'utf-8'  #设置编码
        ratevalue = re.findall(r'"total":([^,]+)',respRate.text,re.I)
        nemax = re.findall(r'"maxPage":([^,]+)',respRate.text,re.I)
        negative=ratevalue[0]
        #if middle == '0' and nemax[0] == '0':    # 判断是淘宝的还是天猫的
            #print ("我是天猫的，我运行了")
            #tmrateload ['itemId'] = pid[i]
            #tmrespRate = requests.get(tmrateUrl, params = tmrateload)
            #tmrespRate.encoding = 'utf-8'  #设置编码
            #json_str = json.dumps(tmrespRate.text)
            #json_data = json.loads(json_str)
            #print (json_str['tags']['tagClouds'][0]['count'])
        current=i+(k*44)
        allcount=limit*44
        print(" 第 " + str(current) + " 条商品数据 -- 总进度：" + str('%.2f'%((current/allcount)*100))+"%")
        try:
            file.write(str(k*44+i+1)+' 商品ID：'+pid[i]+' &&& '+' 商品名称：'+title[i]+' &&& '+'价格：'+price[i]+' &&& '+'地址：'+loc[i]+' &&& '+'销量：'+sales[i]+' &&& '+'好评：'+positive+' &&& '+'中评：'+middle+' &&& '+'差评：'+negative+'\n')
        except: 
            file.write(str(k*44+i+1)+' 商品ID：'+pid[i]+' &&& '+' 商品名称：'+title[i]+' &&& '+'价格：'+price[i]+' &&& '+'地址：'+loc[i]+' &&& '+'销量：'+"0人付款"+' &&& '+'好评：'+positive+' &&& '+'中评：'+middle+' &&& '+'差评：'+negative+'\n')
file.close()
print ("单实例结束时间： "+str(time.time()))




