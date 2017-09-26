'''		
--------------------------------------------------------------
Features to be considered: 
1.products purchased
2.Location
3.company type
4.Sales mode 
5.revenue 
'''


import numpy as np 
import pandas as pd 
from collections import defaultdict
from sklearn.externals import joblib
from datetime import datetime
from sklearn.cluster import KMeans
import nltk
from nltk import word_tokenize 
from collections import Counter


def convert_StringsTo_params(Strinput):
	#input is concatenated strings  
	text = nltk.Text(Strinput)
	text = sorted(set(text))
	return text


def train(input):
	## input = {"file": "data.csv"}
	fileName = input['file']

	xl = pd.ExcelFile(fileName) 


	data = pd.read_excel(fileName, sheetname = xl.sheet_names, header=0,na_values='NA')
	salesData = data['Sales Data']
	productLedger = data['Product Ledger'] 

	countryGroupings =pd.read_excel(fileName, sheetname = 2, header=0,na_values='0')

	salesChannel = salesData['salesChannel'].tolist() 	
	# print convert_StringsTo_params(salesChannel)

	product = salesData['productSold'].tolist()
	# print convert_StringsTo_params(product)

	countryGroupings = countryGroupings.dropna()

	location_feature = []
	for country in salesData['custCountry'].values:
		a = np.where(str(country) == countryGroupings.values[:,[0]])	
		if len(a[0]) == 0:
			location_feature.append('other')
		else:
			location_feature.append(str(countryGroupings.values[[int(a[0])],[1]][0]))
	# print location_feature		
	# print convert_StringsTo_params(location_feature)
	df = pd.DataFrame()
	count = 0 
	for modes in convert_StringsTo_params(salesChannel):
		list1 = []
		for mode in salesChannel:
			if mode == modes:
				list1.append(1)
			else:
				list1.append(0)
		df.insert(count,count,list1)
		count = count + 1

	for products in convert_StringsTo_params(product):
		list1 = []
		for proDucts in product:
			if proDucts == products:
				list1.append(1)
			else:
				list1.append(0)
		df.insert(count,count,list1)
		count = count + 1		

	for location in convert_StringsTo_params(location_feature):
		list1 = []
		for locations in location_feature :
			if locations == location:
				list1.append(1)
			else:
				list1.append(0)
		df.insert(count,count,list1)
		count = count + 1	
	
	#print df	
	


	k = 6
	kmeans = KMeans(n_clusters=k,random_state=0).fit_predict(df)
	
	#create groups of customer id 
	kmeans = pd.DataFrame(kmeans)
	kmeans.insert(1,'ID',salesData['custId'])
	kmeans.insert(2,'product',salesData['productSold'])

	customer_groups = pd.DataFrame()
	for i in range(6):
		list1 = []
		a = np.where(kmeans.values[:,0] == i)
		list1.append(kmeans.values[a,1])
		customer_groups.insert(i,i,list1)
	# print customer_groups	

	product_groups = pd.DataFrame()
	for i in range(6):
		list1 = []
		list2 = []
		a = np.where(kmeans.values[:,0] == i)
		list1.append(kmeans.values[a,2])
		count = list1[0][0].tolist().count('SUPA105')
		product_groups.insert(i,i,list1)

	list1 = []	
	a = np.where(kmeans.values[:,0] == 0)
	list1.append(kmeans.values[a,2])
	for 
		print list1[0][0]
		print list1[0][0].tolist().count('SUPA105')
			
train({"file":"/home/pranav/Documents/my_projects/arrowAI/inclap-sale-prediction/data.xlsx"})
