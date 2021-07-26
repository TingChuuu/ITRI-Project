'''
<<<last post date:2021-03-17>>>
https://www.ptt.cc/bbs/CVS/index2239.html
https://www.ptt.cc/bbs/CVS/index2542.html
'''

#===============================================================================

import grequests
from bs4 import BeautifulSoup
import re
import pandas as pd

#===============================================================================

def get_pagedata(urls):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    reqs = [grequests.get(link,headers=HEADERS,cookies={'over18':'1'}) for link in urls]
    resp = grequests.map(reqs)
    return resp

def get_posturls(resp):
    post_url = []
    
    for r in resp:
        sp = BeautifulSoup(r.text, 'lxml')
        post_info = sp.find_all('div','title')
        
        for i in post_info:
            link_raw = re.findall('(?<=href=").+(?=.html)',str(i),re.S)
            for j in link_raw:
                link = f'https://www.ptt.cc{j}.html'
                post_url.append(link)

    return post_url

#===============================================================================

postlist_url = []
for i in range(2239,2543):
    i = f'https://www.ptt.cc/bbs/CVS/index{i}.html'
    postlist_url.append(i)
# print(postlist_url)

resp=get_pagedata(postlist_url)
post_url=get_posturls(resp)
# print(post_url)

post_url_temp=pd.DataFrame(data=post_url)
post_url_temp.to_excel(r'D:\專題\post_url.xlsx',index=False)



  

