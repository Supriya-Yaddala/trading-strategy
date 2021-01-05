from datetime import datetime
import xlrd,datetime
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

 
# Give the location of the file
loc = (r"C:\Users\priya\Desktop\ROUGH WORK\HINDALCO_1D.xls")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
#connecting to mysql database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="test_db"
)
#open cursor

cur=mydb.cursor()
cur.execute("drop table hdata")


flag=0
for x in cur:
	if "hdata" in x:
		flag=1
		break

#create table	
if flag==0:
	cur.execute("create table hdata(datetime date,close integer,high integer,low integer,\
		open integer,volume integer,instrument varchar(30));")
	print("table created")
	mydb.commit()
else:
	print("table already created")


#insert data into table
for i in range(1,sheet.nrows):
	val=sheet.row_values(i)
	#convert date value into date object
	y = xlrd.xldate_as_tuple(val[0], wb.datemode)
	val[0]=datetime.datetime(y[0],y[1],y[2],y[3],y[4],y[5])
	vtup=(val[0],val[1],val[2],val[3],val[4],val[5],val[6])
	cur.execute("insert into hdata(datetime,close,high,low,open,volume,instrument) \
		values(%s,%s,%s,%s,%s,%s,%s)",val)

mydb.commit()
print("values inserted successfully")
#reading values from database
cur.execute("select close from hdata")

l=[]
for x in cur:
	l.append(x[0])
panddata=pd.DataFrame(l)
panddata['period_9']=panddata[0].rolling(9).mean()
panddata['period_27']=panddata[0].rolling(27).mean()



plt.figure(figsize=(15,10))
plt.grid(True)
plt.plot(panddata[0],label='actualprice')
plt.plot(panddata['period_9'],label='period_9')
plt.plot(panddata['period_27'],label='period_27')
plt.legend(loc=2)
plt.show()




