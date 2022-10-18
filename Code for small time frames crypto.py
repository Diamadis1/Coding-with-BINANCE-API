#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Χρησιμοποίεισαι αυτό τον κώδικα για μικρά time frames σε crypto (Binance API source)
# Για Daily δεδομενα γράψε κώδικα με yahoofinance library
import pandas as pd
from binance.client import Client
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


client = Client()


# In[3]:


info = client.get_exchange_info()


# In[4]:


symbols=[x['symbol']for x in info['symbols']]


# In[5]:


list=[symbol for symbol in symbols if symbol.endswith('USDT')]


# In[6]:


def getdailydata(symbol):
#     Αν θέλεις να παρεις δεδομένα απο το 2017 μέχρι σήμερα χρησιμοποιείς το πρώτο
#     Αν θέλεις συγκεκριμένο timeline χρησιμοποιείς το δεύτερο

#     frame=pd.DataFrame(client.get_historical_klines(symbol,
#                                                    '1d','1 JAN 2011'))
    frame = pd.DataFrame(client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR,
                                          "1 Oct, 2022", "15 Oct, 2022"))
    if len(frame)> 0:
        frame=frame.iloc[:,:5]
        frame.columns=['Time','Open','High','Low','Close']
        frame=frame.set_index('Time')
        frame.index=pd.to_datetime(frame.index,unit='ms')
        frame=frame.astype(float)
        return frame


# In[7]:


# getdailydata('BTCUSDT')


# In[8]:


exclude = ['UP','DOWN','BEAR','BULL']


# In[9]:


non_lev = [symbol for symbol in list if all(
excludes not in symbol for excludes in exclude)]


# In[10]:


# non_lev


# In[11]:


list = ['BTCUSDT','ETHUSDT','DOGEUSDT','XRPUSDT','XMRUSDT','DASHUSDT','NEOUSDT','LTCUSDT',
         'XLMUSDT','ETCUSDT','ZECUSDT','FILUSDT']


# In[12]:


dfs=[]
for coin in list:
     dfs.append(getdailydata(coin))


# In[13]:


mergeddf = pd.concat(dict(zip(list,dfs)), axis=1)


# In[14]:


closesdf = mergeddf.loc[:,mergeddf.columns.get_level_values(1).isin(['Close'])]


# In[29]:


closesdf


# In[16]:


# Άλλη λίστα είναι η διαφορά εδω χρησιμοποιείς την relevant αντι 
# την list που έχεις φτιάξει παραπάνω

# dfs= []

# for coin in relevant:
#     dfs.append(getdailydata(coin))


# In[17]:


# mergeddf = pd.concat(dict(zip(relevant,dfs)), axis=1)


# In[18]:


# closesdf = mergeddf.loc[:,mergeddf.columns.get_level_values(1).isin(['Close'])]


# In[19]:


# closesdf


# In[20]:


closesdf.columns=closesdf.columns.droplevel(1)


# In[21]:


logretdf=np.log(closesdf.pct_change() +1)


# In[22]:


logretdf


# In[23]:


logretdf.corr()


# In[24]:


sns.set(rc={'figure.figsize':(10,10)})
sns.heatmap(logretdf[['BTCUSDT','ETHUSDT','DOGEUSDT','XRPUSDT','XMRUSDT','DASHUSDT','NEOUSDT','LTCUSDT',
         'XLMUSDT','ETCUSDT','ZECUSDT','FILUSDT']].corr())
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.show()


# In[25]:


corr_df = logretdf.corr()
corr_df.filter(non_lev,axis=1)


# In[26]:


stacked = corr_df.filter(non_lev, axis=1).filter(non_lev,axis=0)


# In[27]:


unstacked=stacked.unstack()
unstacked.drop_duplicates()


# In[28]:


unstacked[unstacked < 1].nlargest(20)


# In[ ]:





# In[ ]:




