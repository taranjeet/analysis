from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import *
from django.template import RequestContext
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from xvfbwrapper import Xvfb
from codechef.models import *
from lxml import etree
import urllib
import scrapy
import json
# Create your views here.
"""
	View for displaying the homepage 
"""
def index(request):
	return render_to_response('index.html')

"""
	View for getting the stats of user according to the problems
	solved and the no of tries that he has made in solving a
	particular problem. 
"""
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

"""
	View for getting the stats of user according to the problems
	solved and the no of tries that he has made in solving a
	particular problem. 
"""
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

"""
	View for getting the data of a particuar user according to user search name 
	and then displaying the details of that user as a profile page for that user
	 somewhat similar to codechef.  
"""

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

"""
	View for getting the details of every user such as the college name and 
	the year of joining and many other details.
"""
def userList(request):
	ii=0
	for i in range(1,2234):
		url='http://discuss.codechef.com/users/?sort=name&page='+str(i)
		print url
		page=urllib.urlopen(url).read()
		x=etree.HTML(page)
		usernames=x.xpath("//div[@class='user']/ul/li/a/text()")
		# print usernames
		with open("usernames1.txt","a") as f:
			for user in usernames:
				#print user
				user=user.strip()
				base_url='http://www.codechef.com/users/%s'%(user)
				page1=urllib.urlopen(base_url.encode('utf-8')).read()
				x1=etree.HTML(page1)
				#collegename=x1.xpath('//td/text()')[13].strip()			#not working
				#try this
				#   x1.xpath('//tr/td[../td/b/text()="Institution:"]')
				collegename=x1.xpath('//tr[td/b/text()="Institution:"]/td/text()')
				collegename=''.join(collegename)

				name=x1.xpath('//div[@class="user-name-box"]/text()')
				name=''.join(name)
				if collegename:
					print ii
					ii+=1
					print user,name,collegename
					# pass
					# User(name=name,username=user,collegename=collegename).save()
				# f.write(str(user.encode('utf-8'))+"\n")

"""
	View for adding friends in order to keep track of their activities 
	and probelm solving skills
"""
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

"""
	View for getting the lsit of all the campus chapters that are present on Codechef.
"""
def getChapterList(request):
	vdisplay = Xvfb()
	vdisplay.start()
	driver = webdriver.Firefox()
	driver.get("http://www.codechef.com/campus_chapter/list")
	page = driver.page_source
	x=etree.HTML(page)
	chapterCode = x.xpath("//span[@class='chapter-name']/text()")
	chapterName = x.xpath("//div[@class='cc_listing-textbox-description']/@title")
	chapterStartDate=x.xpath("//div[@class='cc_listing-status']/text()")

	for i in range(0,len(chapterName)):
		College(code=chapterCode[i],name=chapterName[i],date=chapterStartDate[i]).save()
		print chapterName[i]+"   "+chapterCode[i]+' '+chapterStartDate[i]
	driver.close()
	vdisplay.stop()
	return HttpResponse(chapterName)

"""
	View for fetching the details of every user so as to prepare the analytics of Campus chapters
"""

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

"""
	View for updating the details of the Campus Chapters
"""
def updateChapters(request):
	vdisplay = Xvfb()
	vdisplay.start()
	driver = webdriver.Firefox()
	driver.get("http://www.codechef.com/campus_chapter/list")
	page = driver.page_source
	x=etree.HTML(page)
	chapterCode = x.xpath("//span[@class='chapter-name']/text()")
	dbChapterCode = CampusChapter.objects.get.all()
	chapterName = x.xpath("//div[@class='cc_listing-textbox-description']/@title")
	chapterStartDate=x.xpath("//div[@class='cc_listing-status']/text()")
	if chapterStartDate>lastCrawledDate:
		"Then write query for entering that campus chapter into the db."
	"""
		THIS VIEW IS NOT COMPLETED. SO, SKIP IT !!
	"""
	for i in range(0,len(chapterName)):
		College(code=chapterCode[i],name=chapterName[i],date=chapterStartDate[i]).save()
		print chapterName[i]+"   "+chapterCode[i]+' '+chapterStartDate[i]
	driver.close()
	vdisplay.stop()
	return HttpResponse(chapterName)

"""
Documentation here for this view
"""
def campus(request):
	return render_to_response("campus.html",context_instance = RequestContext(request))