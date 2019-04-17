import pandas as pd
import chardet
# 导入五年数据集
df08 = pd.read_csv("C:\\Users\\renxi\\Documents\\Datasets\\2008.csv",encoding='gb18030',low_memory=False)
df09 =  pd.read_csv("C:\\Users\\renxi\\Documents\\Datasets\\2009.csv",encoding='gb18030',low_memory=False)
df10 =  pd.read_csv("C:\\Users\\renxi\\Documents\\Datasets\\2010.csv",encoding='gb18030',low_memory=False)
df11 = pd.read_csv("C:\\Users\\renxi\\Documents\\Datasets\\2011.csv",encoding='gb18030',low_memory=False)
df12 = pd.read_csv("C:\\Users\\renxi\\Documents\\Datasets\\2012.csv",encoding='gb18030',low_memory=False)
# 合成总数据集
df_new = pd.concat([df08,df09,df10,df11,df12],ignore_index =True)
# 数据清洗
#对异常值进行处理
df_new = df_new[(df_new.数量>0)&(df_new.销售价格>0)]
df_new = df_new.dropna(axis = 0)
# 去掉不必要的数据列
df_new = df_new.drop(['店铺编号','店铺地址','店铺简称','货号','货品名称','颜色编号','颜色说明','尺码','销售价格'],axis = 1)
# 筛选上海市的产品
df_new = df_new[df_new[u'店铺省市'].isin([u'上海市上海市市辖区'])]
# 对价格分段
Q1_price = df_new['吊牌价'].quantile(0.33)
Q2_price = df_new['吊牌价'].quantile(0.66)
def price_level (x):
    if x < Q1_price:
        pl = 0
    elif x < Q2_price:
        pl = 1
    else:
        pl = 2
    return pl
df_new['价格等地'] = df_new.apply(lambda x: price_level(x[2]),axis=1)
# 去掉不必要的列
df_new = df_new.drop(['店铺省市','吊牌价'],axis=1)
# 添加价格等地对应的数量
df_new['低价'] = df_new.apply(lambda x : x[1] if x[2]==0 else 0, axis=1 )
df_new['中价'] = df_new.apply(lambda x: x[1] if x[2]==1 else 0, axis=1 )
df_new['高价'] = df_new.apply(lambda x : x[1] if x[2]==2 else 0, axis=1 )
df_new = df_new.drop(['数量','价格等地'],axis=1)
# 对日期按周划分
df_new['销售日期'] = pd.to_datetime(df_new['销售日期'])
df_new.set_index('销售日期', inplace=True)
df_new.sort_index(inplace=True)
output = df_new.resample('W', loffset=pd.offsets.timedelta(days=-6)).sum()
output.to_csv('08-12week_price_division.csv')
