from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from codechef.models import *
from lxml import etree
import scrapy
import urllib
# Create your views here.

def index(request):
	return render_to_response('index.html')

def analysis(request):
	c = {}
	c.update(csrf(request))
	WA=RTE=TLE=CTE=AC=None
	d={}
	if request.POST:
		print 'post request for analysis'
		user=request.POST['user']
		problem=request.POST['problem'].upper()
		print user,problem
		url='http://www.codechef.com/status/%s,%s' % (problem,user)
		print url
		page=urllib.urlopen(url).read()
		x=etree.HTML(page)
		sols=x.xpath('//tr[@class="kol"]')
		WA=len(x.xpath("//span[@title='wrong answer']"))
		RTE=len(x.xpath("//span[@title='runtime error(NZEC)']"))
		AC=len(x.xpath("//span[@title='accepted']"))
		TLE=len(x.xpath("//span[@title='time limit exceeded']"))
		CTE=len(x.xpath("//span[@title='compilation error']"))
		#arr=['WA','RTE','CTE','TLE','AC']
		submission=WA+RTE+AC+TLE+CTE
		d['CTE']=(CTE,100.0*CTE/submission)
		d['AC']=(AC,100.0*AC/submission)
		d['RTE']=(RTE,100.0*RTE/submission)
		d['TLE']=(TLE,100.0*TLE/submission)
		d['WA']=(WA,100.0*WA/submission)
		#print d['CTE']
		if AC>0:
			#it means the problem is solved.
			#get the language
			z=x.xpath('./tr[/span/@title="accepted"]')
			submission_id=x.xpath('//tr/span[contains(@title,"accepted")]/td[1]/text()')
			last_time=x.xpath('//tr[@class="kol"]/td[2]/text()')
			run_time=x.xpath('//tr[@class="kol"]/td[5]/text()')
			mem=x.xpath('//tr[@class="kol"]/td[6]/text()')
			lang=x.xpath('//tr[@class="kol"]/td[7]/text()')
			print submission_id,lang,run_time,mem,last_time,z
		print WA,RTE,AC,TLE,CTE
	return render_to_response('anal.html',{'subs':d},context_instance=RequestContext(request))

def updateProblems(request):
	categories=["easy","medium","hard","challenge","extcontest","school"]
	for i in categories:
		url='http://www.codechef.com/problems/%s' % (i)
		print url
		page=urllib.urlopen(url).read()
		x=etree.HTML(page)
		problemCode = x.xpath('//a[@title="Submit a solution to this problem."]/text()')
		problemName = x.xpath('//div[@class="problemname"]/a/b/text()')
		# print problemName 
		# for j in range (0,len(problemCode)):
		# 	if i=="easy":
		# 		Easy.objects.create(name=problemName[j],code=problemCode[j]).save()
		# 		print problemName[j]," : ",problemCode[j]
		# 	elif i=="medium":
		# 		Medium.objects.create(name=problemName[j],code=problemCode[j]).save()
		# 		print problemName[j]," : ",problemCode[j]
		# 	elif i=="hard":
		# 		Hard.objects.create(name=problemName[j],code=problemCode[j]).save()
		# 		print problemName[j]," : ",problemCode[j]
		# 	elif i=="challenge":
		# 		Challenge.objects.create(name=problemName[j],code=problemCode[j]).save()
		# 		print problemName[j]," : ",problemCode[j]
		# 	elif i=="extcontest":
		# 		Peer.objects.create(name=problemName[j],code=problemCode[j]).save()
		# 		print problemName[j]," : ",problemCode[j]
		# 	elif i=="school":
		# 		School.objects.create(name=problemName[j],code=problemCode[j]).save()
		# 		print problemName[j]," : ",problemCode[j]
	return render_to_response("user.html",{"p":problemName},context_instance=RequestContext(request))