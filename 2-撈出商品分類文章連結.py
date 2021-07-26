
from bs4 import BeautifulSoup
import grequests
import numpy as np
import pandas as pd
import re

#===============================================================================

def get_pagedata(urls):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    reqs = [grequests.get(link,headers=HEADERS,cookies={'over18':'1'}) for link in urls]
    resp = grequests.map(reqs)
    return resp

#===============================================================================

post_url_temp = pd.read_excel(r'D:\專題\post_url.xlsx')
post_url = post_url_temp[0].tolist()

resp=get_pagedata(post_url)

post_date = []
post_title = []
post_url = [] 

for r in resp:
    sp = BeautifulSoup(r.text, 'lxml')   
    
    post_info = sp.select('span.article-meta-value')
    
    try:
        title = (post_info[2].text).lstrip()

        if title[0:4]=='[商品]':
            main_container = sp.select('#main-container')
            
            try:
                post_date.append(post_info[3].text)
            except:
                post_date.append(np.nan)
                
            try:
                post_title.append(title)
            except:
                post_title.append(np.nan)                
            
            for items in main_container: 
                pre_text = items.text.split('--')[0]
                texts = pre_text.split('\n')
                contents = texts[3:]
                content = '\n'.join(contents)

                try:
                    uraw = sp.select('head > link:nth-child(10)')[0]
                    uu = re.findall(r'(?<=https:).+(?=.html)',str(uraw))[0]
                    uu = f'https:{uu}.html'
                    post_url.append(uu)   
                except:
                    post_url.append(np.nan)
                                      
    except:
        title = np.nan
        
pickpost_dict = {
                'Post_date': post_date,
                'Post_title': post_title,
                'Post_url': post_url 
                }

pickpost_temp = pd.DataFrame(pickpost_dict)
pickpost_temp.to_excel(r'D:\專題\productpost_url.xlsx',index=False,encoding='utf-8-sig')


