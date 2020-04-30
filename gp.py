from selenium import webdriver
import time,requests,re,pandas as pd,numpy as np,os
class xinwen:
    def __init__(self,mc):
        self.mc=mc
        self.browser = webdriver.Ie()
        self.browser.get('https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd='+self.mc)

    def huoqv(self):
        f7 = self.browser.find_element_by_id("su")
        f7.click()
        jg1=[]
        jg2=[]
        jg=[]
        f8=self.browser.find_elements_by_xpath("//*[@class=\"c-title\"]")
        f9=self.browser.find_elements_by_xpath("//*[@class=\"c-author\"]")
        for i in f8:
            jg1.append(i.text)
        for i in f9:
            jg2.append(i.text)
        jg=[jg1,jg2]
        return jg
        #f7=browser.find_elements_by_xpath("//*[@class=\"n\"]")翻页
    def shouji(self,jz):
        jz= time.strptime(jz,"%Y-%m-%d")
        jz=365*jz.tm_year+30*jz.tm_mon+jz.tm_mday
        jg1 = []
        jg2 = []
        jg = []
        a=1
        while a:
            f8 = self.browser.find_elements_by_xpath("//*[@class=\"c-title\"]")
            f9 = self.browser.find_elements_by_xpath("//*[@class=\"c-author\"]")
            for i in range(f8.__len__()):
                c1=f8[i].text
                c2=f9[i].text
                c2=c2.split('   ')
                c2=c2[1]
                if c2.find('前')==-1:
                    sj=time.strptime(c2,"%Y年%m月%d日 %H:%M")
                    sj = 365 * sj.tm_year + 30 * sj.tm_mon + sj.tm_mday
                    if sj<jz:
                        a=0
                        break
                jg1.append(c1)
                jg2.append(c2)
            try:
                f7 = self.browser.find_elements_by_xpath("//*[@class=\"n\"]")
                f7[-1].click()
            except:
                a=0
        jg=[jg1, jg2]
        return jg
class thscj:
    def __init__(self):
        self.browser = webdriver.Ie()
    def huoqv(self):
        self.browser.get('http://www.10jqka.com.cn/')
        r=[]
        c = self.browser.find_elements_by_xpath("//*[@zy-fid=\"zy\"]")
        for k in c:
            h=k.text
            if h!='':
                h = h.split('\n')
                r.append(h)
        del r[7]
        return r


class gujia():

    def __init__(self,jiaoyisuo,gupiaodaima):
        if jiaoyisuo == '上证':
            jiaoyisuo = 'sh'
        elif jiaoyisuo == '深证':
            jiaoyisuo = 'sz'
        self.jiaoyisuo=jiaoyisuo
        self.gupiaodaima=gupiaodaima

    def now(self):
        g2={}
        g1=requests.get('http://hq.sinajs.cn/list='+self.jiaoyisuo+self.gupiaodaima)
        g1=g1.text
        g1 = g1.split(',')
        xx=['股票名称','开盘价','收盘价','当前价','今日最高价','今日最低价','买一价','卖一价']
        g2={}
        for k in range(8):
            if k>0:
                g1[k]=float(g1[k])
            g2[xx[k]]=g1[k]
        return g2

    def wfz(self):
        g1 = requests.get('http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol='+self.jiaoyisuo +self.gupiaodaima+'&scale=5&ma=5&datalen=1023')
        g1 = g1.text
        p = re.findall('{.*?}', g1)
        c1 = []
        for i in p:
            c2 = []
            i = re.sub('[{}]', '', i)
            cp = i.split(',')
            for j in range(6):
                j1=re.sub('"', '', re.findall('".*?"', cp[j])[1])
                if j==0:#转换时间格式,str转元组
                    j1 = time.strptime(j1, "%Y-%m-%d %H:%M:%S")
                else:#转换数值
                    j1=float(j1)
                c2.append(j1)
            c1.append(c2)
        c1=c1[2:]
        return c1


sz=gujia('上证','000001').wfz()
sz = np.array(sz)[:, 1:]
df=pd.read_excel('上证50成分股列表.xls',index=None)
x=[]
y=[]
dx=[]
#创建文件夹
try:
    os.makedirs('股票数据/待判断')
    os.makedirs('股票数据/训练数据/1')
    os.makedirs('股票数据/训练数据/0')
except:
    print('已创建文件夹')
#生成数据
for k1 in range(df.shape[0]-40):
    dm=df.values[k1, 0]
    mz=df.values[k1,1]
    c1 = gujia('上证',str(dm)).wfz()
    c2 = np.array(c1)[:, 1:]
    c3=np.array(c1)[:,0].tolist()
    jz=c3[0]
    m1=xinwen(mz)
    jg=m1.shouji(time.strftime("%Y-%m-%d",jz))
    m1.browser.close()
    jg1=jg[1]
    for k2 in range(jg1.__len__()):
        if jg1[k2].find('前') == -1:
            break
    jg=[jg[0][k2:],jg[1][k2:]]
    jg1=jg1[k2:]
    sz1=[]
    for k2 in c3:
        sz1.append(time.mktime(k2))
    b1=[0]*sz1.__len__()
    for k2 in jg1:
        k2 = time.strptime(k2, "%Y年%m月%d日 %H:%M")
        k2=time.mktime(k2)
        for k3 in range(sz1.__len__()):
            if k2<sz1[k3]:
                b1[k3]+=1
                break
    h5 = np.array(b1).reshape(5,48).T
    h5=np.vstack((h5[0:-2,:],np.tile(h5[-1,:]+h5[-2,:],(1,1))))
    for k2 in range(5):
        h1 = c2[48*k2:48*(k2+1),:]
        h2 = (h1[1:, :] - h1[0:-1, :]) / h1[0:-1, :]
        h3=sz[48*k2:48*(k2+1),:]
        h4=(h3[1:, :] - h3[0:-1, :]) / h3[0:-1, :]
        tt=np.tile(h2[:,0], (1, 1)).T
        for k3 in range(5):
            tt= tt = np.hstack((tt, np.tile(h2[:, k3], (1, 1)).T))
            if k3 == 3:
                tt = np.hstack((tt, np.tile(h5[:,k3], (1, 1)).T))
            tt = np.hstack((tt, np.tile(h4[:, k3], (1, 1)).T))

        tt=tt[:,1:]
        tt=pd.DataFrame(tt)
        if k2!=4:
            y1=(c2[48*(k2+2)-1,3]-c2[48*(k2+1)-1,3])/c2[48*(k2+1),3]
            if y1>0:
                tt.to_csv('股票数据/训练数据/1/'+mz+'_'+time.strftime("%Y-%m-%d",c1[48*k2][0])+'.csv',index = False,header = False)
            else:
                tt.to_csv('股票数据/训练数据/0/' + mz + '_' + time.strftime("%Y-%m-%d", c1[48 * k2][0]) + '.csv', index=False,header=False)
        else:
            tt.to_csv('股票数据/待判断/' + mz + '_' + time.strftime("%Y-%m-%d", c1[48 * k2][0]) + '.csv',index=False,header=False)



#jdf=xinwen("京东方")
#x=jdf.huoqv()
#c1=gujia('上证','000725').wfz()
#j=gujia('上证','000725')
#ths=thscj()
#x2=ths.huoqv()
cc=[]

for k in range(x[0].__len__()):
    hh=[x[1][k]]
    hh.append(x[0][k])
    cc.append(hh)
