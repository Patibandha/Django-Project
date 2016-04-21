from django.shortcuts import render
from django.http import HttpResponse
import re

def read(req):
	# Open the file in sorted formate
	f1=(''.join(sorted(open(["File Path"]))))
	# find ',' in a file
	x=re.sub('\n',',',f1)
	# get rid of ','
	data=x.split(',')
	y=len(data)
	dList=[]
	# divede the file data in 4 colon data with indexing
	for i in range(1,y/4+1):
		dic={}
		dicmale={}
		# match the data given in indexed formate and if the data matches it will goes in given dictinary
		for j in range(0,4*i):
			if j==0 or j%4==0:
				dict1={'name':data[j]}
				dic.update(dict1)
			elif j==1 or j%4==1:
				dict2={'age':data[j]}
				dic.update(dict2)
			elif j==2 or j%4 ==2:
				dict3 ={'zipcode':data[j]}
				dic.update(dict3)
			elif j==3 or j%4==3:
				dict4={'gender':data[j]}
				dic.update(dict4)
		# append all the dictinary data in a list
		dList.append(dic)
		
	return render (req,'["Redirect to HTML Page"]',{'dList':dList})