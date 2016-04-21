from django.shortcuts import render
from django.http import HttpResponse
import re

def add(req,na,age,zip,gender):
	# open file in read mode
	a1=open(["File path"], "r+")
	r=a1.read()
	a1.close()
	# now open again in write mode
	b1=open(["File path"], "w")
	# concatenate strings which we have received by URL 
	newdata=na + ',' + str(age) + ',' + str(zip) + ',' + gender
	upFile=r + newdata +'\n'
	b1.write(upFile)
	b1.close()
	return render (req,["HTML page"],{'na':na})