#encoding:utf-8
#-*-coding UTF-8 -*-:

import os 
import csv
from urllib import urlretrieve
import re
import time 
import math

output=file("output.txt",'w')
init_year=2002

close_price=[]
max_close_price=0
minimum_close_price=10000

now_year=time.localtime(time.time()).tm_year
now_month=time.localtime(time.time()).tm_mon
now_day=time.localtime(time.time()).tm_mday

print "=====程式執行中　請稍候===="

for y in range(now_year-init_year+1):
	print y+1,"/",now_year-init_year+1
	years=init_year+y	
	temp_per_year=[]
	for x in range(12):	
		if(years==now_year):
			if(x+1>now_month):
				break
		year=str(years)	
		temp_per_month=[]
		init_sp=0
		if(x<9):
			month="0"+str(x+1)
		else:
			month=str(x+1)
		stock_num="2498"
		FILE_NAME="temp.csv"
		url="http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report"+year+month+"/"+year+month+"_F3_1_8_"+stock_num+".php&type=csv"
		urlretrieve(url,FILE_NAME)
		file=csv.reader(open(FILE_NAME))
		output.write("===="+year+month+"====="+"\n")
		for row in file:
			if(len(row)>6):
				a=re.search('[\d]*,?[\d]*[\.]*[\d]*',row[6])	
				if(len(a.group())>0):
					convert_value=a.group().replace(",","")
					now_price=float(convert_value)
					temp_per_month.append(now_price)
					if(now_price>max_close_price):
						 max_close_price=now_price
					if(now_price<minimum_close_price):
						minimum_close_price=now_price
		os.remove(FILE_NAME)	

		temp_per_year.append(temp_per_month)
	close_price.append(temp_per_year)


a=len(close_price)
b=len(close_price[a-1])
c=len(close_price[a-1][b-1])

today_close_price=close_price[a-1][b-1][c-1]

average_close_price_per_month=[ ]

for i in range(len(close_price)):
	temp_year_mean=[]
	for j in range(len(close_price[i])):
		temp_month_sum=0
		for k in range(len(close_price[i][j])):
			temp_month_sum=temp_month_sum+close_price[i][j][k]
		if(len(close_price[i][j])>0):
			temp_month_sum=temp_month_sum/len(close_price[i][j])
			temp_year_mean.append(temp_month_sum)
	average_close_price_per_month.append(temp_year_mean)


positive_price=[  ]
negative_price=[  ]

for i in range(len(average_close_price_per_month)):
	for j in range(len(average_close_price_per_month[i])):
			sub=0
			if(j==0):
				if(i!=0):
					sub=average_close_price_per_month[i][j]-average_close_price_per_month[i-1][len(average_close_price_per_month[i-1])-1]
			else:
				sub=average_close_price_per_month[i][j]-average_close_price_per_month[i][j-1]
		
			if(sub>0):
				positive_price.append(sub)
			if(sub<0):
				negative_price.append(sub)

temp_value=0

for i in range(len(positive_price)):
	temp_value=temp_value+positive_price[i]

if(len(positive_price)>0):
	positive_price_mean=temp_value/len(positive_price)



temp_value=0
for i in range(len(negative_price)):
	temp_value=temp_value+negative_price[i]

if(len(negative_price)>0):
	negative_price_mean=temp_value/len(positive_price)

print "=======程式執行完成======="


print "今天日期:",
print now_year,
print "/",
print now_month,
print "/",
print now_day

print "今日股價:",
print today_close_price


print "最高股價:",
print max_close_price

print "最低股價:",
print minimum_close_price


print "平均漲幅:",
print positive_price_mean

print "漲的次數:",
print len(positive_price)

print "平均跌幅:",
print negative_price_mean

print "跌的次數:",
print len(negative_price)


float_positive_len=float(len(positive_price))
float_negative_len=float(len(negative_price))

positive_frequency_ratio=round(float_positive_len/float_negative_len)
negative_frequency_ratio=round(float_negative_len/float_positive_len)


print "平均漲",positive_frequency_ratio,"次就會跌",negative_frequency_ratio,"次"

substration=positive_frequency_ratio*positive_price_mean + negative_frequency_ratio*negative_price_mean


if(substration>=0):
	print "平均每",positive_frequency_ratio+negative_frequency_ratio,"個月會漲",substration,"元"
else:
	
	print "平均每",positive_frequency_ratio+negative_frequency_ratio,"個月會跌",-substration,"元"

prediction_price=float(500)

best_condition=(prediction_price-float(today_close_price))/positive_price_mean

print "若是今天開始穩定成長 要",round(best_condition),"個月後才能超過",prediction_price,"元"

mean_condition=(prediction_price-float(today_close_price))/substration
mean_condition=mean_condition*2

print "若是今天開始平均成長 要",round(mean_condition),"個月後才能超過",prediction_price,"元"
