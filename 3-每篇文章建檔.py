
from bs4 import BeautifulSoup
import grequests
import numpy as np
import pandas as pd
import re
import string


#===============================================================================

def get_pagedata(urls):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    reqs = [grequests.get(link,headers=HEADERS,cookies={'over18':'1'}) for link in urls]
    resp = grequests.map(reqs)
    return resp

def strQ2B(s):
    """把字串全形轉半形"""
    rstring = ""
    for uchar in s:
        u_code = ord(uchar)
        if u_code == 12288:  # 全形空格直接轉換
            u_code = 32
        elif 65281 <= u_code <= 65374:  # 全形字元（除空格）根據關係轉化
            u_code -= 65248
        rstring += chr(u_code)
    return rstring


#===============================================================================

# post_url_temp = pd.read_excel(r'D:\專題\productpost_url.xlsx')
post_url_temp = pd.read_excel(r'/Users/chuhsinan/Downloads/專題/productpost_url.xlsx')
post_url = post_url_temp['Post_url'].tolist()

resp=get_pagedata(post_url)

post_date = []
post_author = [] 
post_url = [] 
company = [] 
product = []
price = [] 
score = [] 
review = []
commentscore = []
likenum = []
likect = []
neunum = []
neuct = []
boonum = []
booct = []
pusherrnum = []


for r in resp:
    sp = BeautifulSoup(r.text, 'lxml')    
    post_info = sp.select('span.article-meta-value')
    
    try:
        title = sp.select('#main-content > div:nth-child(3) > span.article-meta-value')[0].text

        main_container = sp.select('#main-container')
        
        post_date.append(post_info[3].text)
        post_author.append(post_info[0].text)            
        
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
            
            try:
                co = re.findall('(?<=【便利商店/廠商名稱】：).+(?=【規)', content,re.S)[0].replace('\n','').lstrip()
                sv = ['7-11','711','7/11','小七','小7','統一','seven','7-Eleven','7-ELEVEN']
                fm = ['全家','FamilyMart']
                ok = ['ok','Ok','OK']
                hl = ['萊爾富','Hi-Life']
                if [i for i in sv if i in co]:
                    ck='711'
                    company.append(ck)
                elif [i for i in fm if i in co]:
                    ck='全家'
                    company.append(ck)
                elif [i for i in ok if i in co]:
                    ck='OK'
                    company.append(ck)
                elif [i for i in hl if i in co]:
                    ck='萊爾富'
                    company.append(ck)  
                else:
                    company.append('其他')
            except:
                company.append(np.nan)
                
            try:
                pdc = re.findall('(?<=\s).+', title)[0].replace(ck,'').lstrip()
                pdc = strQ2B(pdc)
                pdc = ''.join([i for i in pdc if i not in string.punctuation])
                product.append(pdc)

            except:
                product.append(np.nan)
    
            try:
                prc = re.findall('(?<=價格】：).+(?=【便)', content,re.S)[0].replace('\n','').lstrip()
                prc = max(map(int,re.findall('\d+', prc)))
                price.append(prc)               
            except:
                price.append(np.nan)
            
            
            try:
                sc = re.findall('(?<=【評分】：).+(?=【心)', content,re.S)[0].replace('\n','').lstrip()
                sc = int(re.findall('\d+', sc)[0])
                score.append(sc)
            except:
                score.append(np.nan)
                
            try:
                r = re.findall('(?<=【心得】：).+', content,re.S)[0].lstrip()
                review.append(r)
            except:
                review.append(np.nan)
        
        
        g, b, n, pusherr = 0, 0, 0, 0
        liket, neut, boot = '', '', ''
    
        for tag in sp.select('div.push'):
            
            try:
                # push_tag  推文標籤  推  噓  註解(→)
                push_tag = tag.find("span", {'class': 'push-tag'}).text
    
                # push_content 推文內容
                push_content = tag.find("span", {'class': 'push-content'}).text
                push_content = push_content[1:].lstrip()
    
                # 計算推噓文數量 g = 推 , b = 噓 , n = 註解
                if push_tag == u'推 ':
                    g += 1
                    liket = liket+push_content+'\n'
                elif push_tag == u'噓 ':
                    b += 1
                    boot = boot+push_content+'\n'
                else:
                    n += 1
                    neut = neut+push_content+'\n'
            except:
                pusherr += 1
                
        cmsc = g-b
        
        commentscore.append(cmsc)
        likenum.append(g)
        likect.append(liket)
        neunum.append(n)
        neuct.append(neut)
        boonum.append(b)
        booct.append(boot)
        pusherrnum.append(pusherr)                 
                
    except:
        title = np.nan
        
form_dict = {
            'Date': post_date,
            'Author': post_author, 
            'Post_url': post_url, 
            'CVS': company, 
            'Product': product,
            'Price': price, 
            'Score': score,
            'Review': review,
            'Comment_Score' : commentscore,
            'Likes' : likenum,
            'Like_Comment' : likect,
            'Neu' : neunum,
            'Neu_Comment' : neuct,
            'Boos' : boonum,
            'Boo_Comment' : booct,
            'Commenterr' : pusherrnum
            }

form_temp=pd.DataFrame(form_dict)

ix=0
for i in form_temp['Date']:
    form_temp.iloc[ix,0] = i[4:10]+' '+i[20:]
    ix=ix+1
# form_temp.to_csv(r'D:\專題\Report.csv',index=False,encoding='utf-8-sig')
form_temp.to_csv(r'/Users/chuhsinan/Downloads/專題/Report.csv',index=False,encoding='utf-8-sig')
# form_temp.to_excel(r'D:\專題\Report_ii.xlsx',index=False,encoding='utf-8-sig')
