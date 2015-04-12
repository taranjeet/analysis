from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from lxml import etree
import urllib
from django.template import RequestContext
# Create your views here.

def index(request):
	return render_to_response('index.html')

def analysis(request):
	c = {}
	c.update(csrf(request))
	WA=None
	RTE=None
	TLE=None
	CTE=None
	AC=None
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
		d['CTE']=100.0*CTE/submission
		d['AC']=100.0*AC/submission
		d['RTE']=100.0*RTE/submission
		d['TLE']=100.0*TLE/submission
		d['WA']=100.0*WA/submission
		#print d['CTE']
		print WA,RTE,AC,TLE,CTE
	return render_to_response('anal.html',{'subs':d},context_instance=RequestContext(request))