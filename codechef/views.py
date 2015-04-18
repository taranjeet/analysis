from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import *
from django.template import RequestContext
from codechef.models import *
from lxml import etree
import urllib
import scrapy
import json
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

def user(request):
	WA=RTE=TLE=CTE=AC=None
	details={}
	if request.POST:
		print 'post request for analysis'
		user=request.POST['user']
		url='http://www.codechef.com/users/%s' % (user)
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
	return render_to_response("user.html",context_instance=RequestContext(request))

def userDetails(request):
	if request.POST:
		username = request.POST['username']
		url = 'http://codechef.com/users/'+str(username)
		u = {"easy":0,"medium":0,"hard":0,"challenge":0,"school":0,"peer":0,"other":0}
		# easy= medium=hard=peer=school=challenge=0
		page=urllib.urlopen(url).read()
		x=etree.HTML(page)
		profile_pic=x.xpath("//div[@class='user-thumb-pic']/img/@src")
		profile_pic = "http://codechef.com"+str(profile_pic[0])
		problems=x.xpath("//tr/td/p/span/a/text()")
		for problem in problems:
			if Easy.objects.filter(code=str(problem)).count()==1:
				u['easy']+=1
			elif Medium.objects.filter(code=problem).count()==1:
				u['medium']+=1
			elif Hard.objects.filter(code = problem).count()==1:
				u['hard']+=1
			elif Peer.objects.filter(code = problem).count()==1:
				u['peer']+=1
			elif School.objects.filter(code = problem).count()==1:
				u['school']+=1
			elif Challenge.objects.filter(code = problem).count()==1:
				u['challenge']+=1
		u['other'] = len(problems)-u['easy']-u['medium']-u['hard']-u['challenge']-u['peer']-u['school']
		u = json.dumps(u, ensure_ascii=False)
		print u
		return render_to_response("userDetails.html",{'u':u,'profile_pic':profile_pic},context_instance= RequestContext(request))
		# return HttpResponse("EASY "+str(easy)+"\n Medium  "+str(medium)+"\n Hard  "+str(hard))
	return render_to_response("userDetails.html",context_instance = RequestContext(request))
	
def userList(request):
	for i in range(1,2219):
		url='http://discuss.codechef.com/users/?sort=name&page='+str(i)
		print url
		page=urllib.urlopen(url).read()
		x=etree.HTML(page)
		usernames=x.xpath("//div[@class='user']/ul/li/a/text()")
		# print usernames
		with open("usernames.txt","a") as f:
			for user in usernames:
				print user
				f.write(str(user.encode('utf-8'))+"\n")

def addFriends(request):
	if request.POST:
		friends = request.POST['friends']
		friends = friends.split(",")
		data = []
		for friend in friends: 
			data.append(fetchUserDetails(str(friend)))
		print data
		return render_to_response("friends.html",{"data":data},context_instance = RequestContext(request))
	return render_to_response("friends.html",context_instance = RequestContext(request))

def getChapterList(request):
	url = 'http://www.codechef.com/campus_chapter/list'
	u = {"chapterName":'',"code":"","chapterUrl":""}
	page=urllib.urlopen(url).read()
	x=etree.HTML(page)
	chapterName = x.xpath("//div[@class='cc_listing-textbox-description']/@title")
	# print u["chapterName"]
	print chapterName
	code=x.xpath("//span[@class='chapter-name']/text()")
	print code
	# u['code'] = "http://codechef.com"+str(profile_pic[0])
	# chapterUrl = "http://www.codechef.com/campus_chapter/"+ str()
	return HttpResponse(chapterName + code)
def fetchUserDetails(friend):
	url = 'http://codechef.com/users/'+str(friend)
	u = {"username":str(friend),"name":"","profile_pic":"","easy":0,"medium":0,"hard":0,"challenge":0,"school":0,"peer":0,"other":0}
	# easy= medium=hard=peer=school=challenge=0
	page=urllib.urlopen(url).read()
	x=etree.HTML(page)
	u['name'] = (x.xpath("//div[@class='user-name-box']/text()"))[0]
	print u["name"]
	profile_pic=x.xpath("//div[@class='user-thumb-pic']/img/@src")
	u['profile_pic'] = "http://codechef.com"+str(profile_pic[0])
	problems=x.xpath("//tr/td/p/span/a/text()")
	for problem in problems:
		if Easy.objects.filter(code=str(problem)).count()==1:
			u['easy']+=1
		elif Medium.objects.filter(code=problem).count()==1:
			u['medium']+=1
		elif Hard.objects.filter(code = problem).count()==1:
			u['hard']+=1
		elif Peer.objects.filter(code = problem).count()==1:
			u['peer']+=1
		elif School.objects.filter(code = problem).count()==1:
			u['school']+=1
		elif Challenge.objects.filter(code = problem).count()==1:
			u['challenge']+=1
	u['other'] = len(problems)-u['easy']-u['medium']-u['hard']-u['challenge']-u['peer']-u['school']
	u = json.dumps(u, ensure_ascii=False)
	return u
