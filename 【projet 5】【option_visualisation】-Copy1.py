
# coding: utf-8

# ### Option_PUT

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas

get_ipython().run_line_magic('matplotlib', 'inline')
#让图表直接在Jupyter Notebook中展示出来 
plt.rcParams['font.sans-serif'] = 'SimHei' # 解决中文乱码问题 
plt.rcParams['axes.unicode_minus'] = False # 解决负号无法显示的问题 
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg' # 矢量图，更清晰")


# #infos: 
# option PUT: 
# 1. contrat d'achat: prix d'exercice=100,prime=6,71
# 2. contrat de vente: PE=110, prime=13,55
# même durée et même echéancce, le prix du support = 95, les 2 contrats sont tous exercés

# In[4]:


#  坐标轴：axe de coordonnées
'''
vlines(x, ymin, ymax)
hlines(y, xmin, xmax，linestyles)
    linestyles : {'solid', 'dashed', 'dashdot', 'dotted'}, optional
'''
# x0=np.linspace(-10,150,1000)
# y0=np.array([0])+x0*0
# plt.plot(x0,y0,'c:')  #画出0轴,复杂版本

plt.vlines(0, -100, 160,'c',linestyles='dotted')
plt.hlines(0, -10, 160,'c',linestyles='dotted')



# 正式画图：
#PUT -achat:  y=-x+93.29
x1=np.linspace(0,150,1000)
interval0=[1 if (0<=i and i<=100) else 0 for i in x1]
interval1=[1 if (i>100) else 0 for i in x1]


a1=93.29
b1=np.array([-6.71])
y1=(a1-x1)*interval0+b1*interval1
'''
重要：
为什么不可以直接写常数（-6.71）或者float(-6.71): 
是因为该计算为numpy数组相乘，需要数组*数组！！！！
'''
plt.plot(x1,y1,'r')


# PUT -vente:  y=x+96.45 
x2=np.linspace(0,150,1000)
interval2=[1 if (0<=i and i<=110) else 0 for i in x1]
interval3=[1 if (i>110) else 0 for i in x1]

a2=-96.45
b2=np.array([13.55])
y2=(x2+a2)*interval2+b2*interval3

plt.plot(x2,y2,'b')





#坐标轴设置
plt.yticks([93.29,0,-6.71,-96.45],[93.29,0,-6.71,96.45])
plt.xticks([0,25,50,75,96.45,110],[0,25,50,75,96.45,110])

plt.title("stratégie de l'option")

plt.tight_layout()#订正：解决x轴标签过大，保存图片显示不全的问题
plt.savefig('picture/【projet 5】option_PUT.png',dpi=500)#订正不清晰：指定分辨率plt.savefig(dpi=500)

