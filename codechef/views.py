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
import datetime
import requests
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

	#get how many pages are there
	user_url='http://discuss.codechef.com/users/?sort=newest'
	page=urllib.urlopen(user_url).read()
	x2=etree.HTML(page)
	till_now=int(x2.xpath('//a[@class="page"]/text()')[4])
	in_db=PageCount.objects.get().sort_newest_count
	if in_db==0:
		#it means that this is the first time we are running this
		#so run the loop till 'till_now'
		limit=till_now
	else:
		#run from 1 till till_now-in_db+1
		limit=till_now-in_db+1




	for i in range(1,limit):
		url='http://discuss.codechef.com/users/?sort=name&page='+str(i)
		print url
		page=urllib.urlopen(url).read()
		x=etree.HTML(page)
		usernames=x.xpath("//div[@class='user']/ul/li/a/text()")
		# print usernames
		with open("usernames.csv","a") as f:
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
					f.write(str(user.encode('utf-8'))+","+str(name.encode('utf-8'))+","+str(collegename.encode('utf-8'))+"\n")

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

this view will return the list of all college campus chapter
"""
def campus(request):
	c = {}
	c.update(csrf(request))
	col=College.objects.all()
	return render_to_response("campus.html",{'college':col},context_instance = RequestContext(request))

def chapter(request):
	'''
	this views needs to be done as a url,
	'''
	contest_codes={1:"JAN",2:"FEB",3:"MARCH",4:"APRIL",5:"MAY",6:"JUNE",7:"JULY",8:"AUG",9:"SEPT",10:"OCT",11:"NOV",12:"DEC"}

	if request.GET:
		code=request.GET['code']
		print 'get request',code
		
	c=College.objects.filter(code=code)
	for i in c:
		collegename=i.name
	print collegename

	#now get all user of this college
	users=User.objects.all().filter(collegename=collegename)
	print len(users)
	#check ranking for LONG contest here
	now=datetime.datetime.now()
	month=now.month
	year=now.year
	day=now.day
	first_friday=find_first_friday(1,month,year)
	if day<first_friday:
		contest_code=contest_codes[month-1]+str(year%2000)
	else:
		contest_code=contest_codes[month]+str(year%2000)
	
	filters = {'filterBy':'Institution='+str(collegename),'order':'asc','sortBy':'rank'}
	page = requests.get("http://www.codechef.com/rankings/"+str(contest_code), params = filters)
	print page.url
	# rankings_url=urllib.quote_plus('www.codechef.com/rankings/%s?filterBy=%s&order=asc&sortBy=rank'%(contest_code,collegename))
	#now if the current date is less than first_friday then dont include this month long rating, instead
	#show him the rating for just previous month
	return HttpResponse('no of users of this college are %s'%(len(users)))



def find_first_friday(day,month,year):
	'''this view will return the date of first friday for LONG challenges'''
	#using sakamoto algorithm
	t=[0,3,2,5,0,3,5,1,4,6,2,4]
	year-=month<3
	index=(year+year/4-year/100+year/400+t[month-1]+day)%7
	date=(5-index+7+1)
	if date>7:
		date-=7
	print index,date



