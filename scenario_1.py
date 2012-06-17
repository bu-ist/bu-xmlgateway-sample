#!/usr/local/bin/python
import os
import cgi, cgitb
from bu_xmlgateway.xmlgateway import VendorRequest
request = VendorRequest()

request.setUrl("http://www-devl.bu.edu/link/bin/uiscgi_demo_xmlgateway_xml.pl")
request.setParameter("ModuleName", "get_building.pl")

form = cgi.FieldStorage()
buildingCd = form.getvalue('BuildingCd')
request.setParameter('BuildingCd', buildingCd);
#request.setParameter('BuildingCd', 'MET');
response = request.getResponse()
print "Content-type: text/html"
print
if request.isError() :
	errorMsg = request.getErrorMsg()       
	print "<h3>System Error</h3>%s \n" % errorMsg
elif response.getType() == 'DATA':
	buildingName	= response.getParameter('BuildingName')
	buildingLoc	= response.getParameter('BuildingLoc')
	print """<html>
		<head><title>Building Description(Python)</title></head>
			<body>
				<h3>BUILDING DESCRIPTION(Python)</h3>				<hr>
				<form action="scenario_1.py" method="POST">
					Building Code:       <input type="text" name="BuildingCd" value="%s">
					<input type="submit" value="Send">
				</form>
				<p>Building Name: <b>%s</b></p>
				<p>Building Location: <b>%s</b></p>
				</body></html>""" % (buildingCd, buildingName, buildingLoc,)

elif response.getType() == 'ERROR':
		print response.getHtml()