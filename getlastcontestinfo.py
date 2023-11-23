from bs4 import BeautifulSoup
from lxml import etree
import openpyxl
import requests
import time
def usex_pathfind(html,name):
    e_html=etree.HTML(html)
    urls_name=e_html.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tbody/tr[1]/td[2]/a/text()')
    urls_rank=e_html.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tbody/tr[1]/td[4]/a/text()')
    urls_solve=e_html.xpath('//*[@id="pageContent"]/div[4]/div[6]/table/tbody/tr[1]/td[5]/a/text()')
    contestmess={}
    if len(urls_name)==0:
        contestmess['statu']='False'
        contestmess['name']=name
        print(contestmess)
        return contestmess
    else:
        contestmess['statu']='Ture'
    # print(type(urls_name[0]))
    contestmess['contestname']=urls_name[0].strip()
    contestmess['rank']=int(urls_rank[0].strip())
    contestmess['solve']=urls_solve[0].strip()
    contestmess['name']=name
    print(contestmess)
    return contestmess
def getuserlastcontest(name):
    request=requests.get('https://codeforces.com/contests/with/'+name)
    request.encoding='utf-8'
    return usex_pathfind(request.text,name)
def getlastcontestrank(contestname,username):
    rank=[]
    for name in username:
        con=getuserlastcontest(name)
        if con['statu']=='Ture' and con['contestname']==contestname:
            rank.append(con)
    ranks=sorted(rank,key= lambda rk : rk['rank'],reverse=False)
    return ranks
def getsname():
    sname=[]
    workbook=openpyxl.load_workbook('qq-cfid.xlsx')
    ws=workbook.active
    sheet2=workbook['Sheet2']
    ecname=sheet2['A']
    for name in ecname:
        sname.append(name.value)
        # print(name.value)
    return sname
def getlastcontestname():
    response = requests.get('https://codeforces.com/api/contest.list?contests=true')
    con=response.json()
    now=time.time()
    for tmp in con['result']:
        startTimeSeconds=tmp['startTimeSeconds']
        if startTimeSeconds<now:
            return tmp['name']
def getlastcontest():
    sname=getsname()
    lastcontestname=getlastcontestname()
    rank=getlastcontestrank(lastcontestname,sname)
    print(rank)
    return rank