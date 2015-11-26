#!/usr/bin/python
from bs4 import BeautifulSoup
import requests, requests.utils, pickle
import os.path
import json
import re
"""
	TODO:
		logger-module to debug info
		defines url in dict
"""
class OWA_Contacts:
	def __init__(self, username, password, cookie_jar):
		self.username = username
		self.password = password
		self.cookie_jar = cookie_jar

		# Create session to handle cookies between requests
		self.session = requests.Session()

		# Pretend we're just a normal browser
		self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'})


	def __searchForName(self, needle):
	        canary = self.session.cookies['UserContext']
	        payload = '<params><canary>' + canary + '</canary><AddMenuMarkup>1</AddMenuMarkup><AddRecipientResults>1</AddRecipientResults><n>' + needle + '</n></params>'
	        r = self.session.post('https://webmail.sdu.dk/owa/ev.owa?oeh=1&ns=RecipWell&ev=ResolveOneRecipientForAnrMenu', data=payload)

		return r.text, r.status_code

	def SearchForName(self, needle):
		# Import cookies if cookiejar exists	
		if self.__cookieExsits():
			self.__loadCookies()
		else:
			self.__getCookies()

		# Look for needle in AD
		result, status_code = self.__searchForName(needle)

		# Nah, we better update the cookie
		if status_code == 440:
			self.__getCookies()

		# Let's try again
		result, status_code = self.__searchForName(needle)

		# Cookies still not valid, let's just exit
		if status_code == 440:
			exit("Unable to renew cookie..")

		# Let's parse zum' of dat' HTML
		matchObj = re.findall( r'Recip\((.*?)\)', result.encode('utf-8').replace('\\','').replace('/','').replace('"','') )
		people = [ person.split(',') for person in matchObj if "Exchange Administrative Group" not in person]
		people =  [ {'name' : person[0], 'email' : person[2] } for person in people]

		return people

	def __saveCookies(self):
		with open(self.cookie_jar, 'w') as f:
			pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

	def __cookieExsits(self):
		return os.path.isfile(self.cookie_jar) 

	def __loadCookies(self):
		with open(self.cookie_jar) as f:
			cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
			self.session.cookies = cookies

	def __getCookies(self):
		# Clear cookies, they're old anyways -  why would we else update them ? 
		self.session.cookies.clear()

		# Get cookie we need in POST request
		self.session.get('https://webmail.sdu.dk/')

		url = 'https://webmail.sdu.dk/owa/auth.owa'
		payload = {'username': self.username, 'password': self.password, 'destination' : 'https://webmail.sdu.dk/owa/', 'flags' :'0', 'isUtf8':'1', 'trusted':'0', 'forcedownlevel':'0'}
		r = self.session.post(url, data=payload, cookies=dict( PBack='0', tzid="Romance Standard Time") )

		if "browser settings must allow scripts to run" in r.text:
			exit("Unable to login, wrong credentials")

		self.__saveCookies()

if __name__ == "__main__":
	owa_contacts = OWA_Contacts("sdu\test13","secretpass", 'cookies_OWA')
	people = owa_contacts.SearchForName("mathias")

	for person in people:
		print person
