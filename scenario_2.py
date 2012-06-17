#!/usr/local/bin/python
import os
import cgi, cgitb
import Cookie
from bu_xmlgateway.xmlgateway import VendorRequest
BU_SESSION_COOKIE_NAME = "bu_session"
cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
try:
	test = cookie["__utma"].value
	session =  cookie[BU_SESSION_COOKIE_NAME].value
except (Cookie.CookieError, KeyError):
    session = ""

# instantiate object
request = VendorRequest()
request.setUrl("http://www-devl.bu.edu/link/bin/uiscgi_shared_xml.pl")
request.setSession(session)

form = cgi.FieldStorage() 
request.setParameter('ModuleName', form.getvalue('ModuleName'));
request.setSyncUrl('')
response = request.getResponse()
session1 = response.getSession()
cookie[BU_SESSION_COOKIE_NAME] = session1
cookie[BU_SESSION_COOKIE_NAME]["domain"] = ".bu.edu"
cookie[BU_SESSION_COOKIE_NAME]["path"] = "/"
print cookie.output()


if request.isError() :
	errorMsg = request.getErrorMsg()
	print "<h3>System Error</h3>%s \n" % errorMsg
elif response.getType() == 'LOGIN':
	print response.getHtml()
elif response.getType() == 'DATA':
	userAlias	= response.getAlias()
	userId		= response.getId()
	userName	= response.getName()
	userEmail	= response.getEmail()
	print "Content-Type: text/html\n\n"	
	print "<html><head><title>User Information(Python)</title></head><body>"
	print "<h3>USER INFORMATION(Python)</h3><br>"
	print "<hr>"
	print "<p><b>User Alias:</b>%s</p>" % userAlias
	print "<p><b>User Id:</b>%s</p>" % userId
	print "<p><b>User Name:</b>%s</p>" % userName
	print "<p><b>User Email:</b>%s</p>" % userEmail
	print "</body></html>"

elif response.getType() == 'ERROR':
	print response.getHtml()
