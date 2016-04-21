from django.shortcuts import render
from django.http import HttpResponse
import re

def remove(req,de):
	f1=open(["File path"], "r+")
	r= f1.read()
	x=re.sub('\n',',',r)
	data=x.split(',')
	y=len(data)
	dStr=''
	f1.close()
	# Read and save data in respected given dictionary
	for i in range(1,y/4+1):
		dic={}
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
		# now we will match the given name with data retrived with dictionary
		if dic['name']== de:
			del dic
			leftData=''
		else:
			n=dic['name']
			a=dic['age']
			z=dic['zipcode']
			g=dic['gender']
			# if the given name is not match with data which is availble in a file it will write again all file
			leftData = n + ',' + a + ','+ z +','+ g + '\n'
		dStr=dStr+leftData
	b1=open(["File path"], "w")
	b1.write(dStr)
	b1.close()
	return render (req,["HTML page"],{'dList':de})