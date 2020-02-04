
# coding: utf-8

# In[17]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts 
import openpyxl
#print(tushare.__version__)#1.2.48
ts.set_token('5b1c11680dd6b8ed4b2ff28bea1d3806605e99e11cfa44b5e303173c')

from IPython.core.interactiveshell import InteractiveShell
import openpyxl
InteractiveShell.ast_node_interactivity = "all"

pd.set_option('max_columns',1000)
pd.set_option('max_row',30)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

get_ipython().run_line_magic('matplotlib', 'inline')
#让图表直接在JupyterNotebook中展示出来 
plt.rcParams['font.sans-serif'] = 'SimHei' # 解决中文乱码问题 
plt.rcParams['axes.unicode_minus'] = False # 解决负号无法显示的问题 
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg' # 矢量图，更清晰")


# In[2]:


#市场代码	说明
# MSCI	MSCI指数
# CSI	中证指数
# SSE	上交所指数
# SZSE	深交所指数
# CICC	中金所指数
# SW	申万指数
# OTH	其他指数

#所有指数基本信息：指数代码     #########################################
pro = ts.pro_api()
a = pro.index_basic(market='SZSE')
a.to_excel(r'export/SZSE指数ex.xlsx', sheet_name='szse指数ex')
#FileNotFoundError: [Errno 2] No such file or directory: 'export/SZSE指数ex.xlsx'
#订正：我现在在“封装函数”路径下,新建封装函数下export
a.head()
a.iloc[3, 0]


# In[32]:


#接上一条：指数代码--->指数数据（日线）  ##########################################
#excel 手动修改，
filename1 = 'SZSE指数ex'  #变量1
sheetname1 = '一级行业指数'  #变量2
b = pd.read_excel(r'export/{}.xlsx'.format(filename1),
                  sheet_name=sheetname1)  #变量1 #变量2

b.reset_index(drop=['index'], inplace=True)
print(b.head())

c = pd.DataFrame()
start='20110101'#变量3
end='20200116'#变量4
for i in range(len(b)):
    try:
        d = pro.index_daily(
            ts_code=b.iloc[i, 0],
            #d = pro.index_daily(ts_code='b.iloc[i,0]',错误！！！没数据，b.iloc不能直接放在引号里啊！不用放引号里，直接就是str
            start_date=start, #变量3
            end_date=end,     #变量4
            fields='ts_code,close,trade_date')

        d.rename(columns={'close': b.iloc[i, 1]}, inplace=True)
        d.drop(columns='ts_code', inplace=True)  #替换name，去掉ts_code
        #print(d)
    except:
        time.sleep(60)
    else:
        if i == 0:
            c = d
            print(c)
        else:
            c = pd.merge(c, d, how='outer')
result = c

#后面不在循环，注意缩进
# b.drop(columns='ts_code',inplace=True)
# b.T

# result = pd.merge(b, c, on='ts_code', how='outer')
# result.reset_index(drop='index')
result.to_excel(r'export/szse综合指数{}_{}.xlsx'.format(start[0:4],end[0:4]),
                sheet_name='深交所{}_{}综合指数日线'.format(start[0:4],end[0:4]))
#print(c)


# In[ ]:


#接上：数据预处理，NaN
result.dropna(axis=1, inplace=True)
#type(result)
#报错：result[:,[1,3]]  不能切片索引获取列，直接列名称
#正确切片：result=result[['name','close']]

#result.reset_index(drop='index',inplace=True)
result.head()
#result.to_excel(r'export/szse综合指数{}_{}删除缺失值.xlsx'.format(start[0:4], end[0:4]),
                #sheet_name='深交所{}_{}{}日线'.format(start[0:4], end[0:4],sheetname1))


# In[57]:


#XX指数相关性
x= result.corr()

#热力图
fig=plt.Figure(figsize=(2000,2000))
cmap=plt.cm.Reds #配色
ax1=plt.imshow(x,cmap=cmap) #订正：是x或者result.corr(),不是result
ax1

plt.colorbar() #订正：colorbar 要放在imshow热力图后显示

industry=x.columns.values#获取替换的名称
tickmarks=np.arange(len(industry))#修改轴的数字与名称个数一一对应
plt.xticks(tickmarks,industry,rotation=90)#x轴替换
plt.yticks(tickmarks,industry,rotation=0)#y轴

#plt.tick_params(size=30) 刻度尺，那条小杠杠
#ax1.set_yticks(np.arange(60)) 不懂
plt.tick_params(axis='both',which='major',labelsize=4)  #####设置坐标轴字号！！！！！
plt.title('SZSE{}{}_{}'.format(sheetname1,start[0:4],end[0:4]))#SZSE 某某指数几几年_几几年

plt.xlabel('x轴',fontsize=3)
plt.tight_layout()#订正：解决x轴标签过大，保存图片显示不全的问题

plt.savefig('export/picture/{}{}_{}_corr.png'.format(sheetname1,start[0:4],end[0:4]),dpi=800)
#订正不清晰：指定分辨率plt.savefig(dpi=500)

