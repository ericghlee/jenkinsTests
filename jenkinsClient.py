#!/usr/bin/python
import json, urllib2, sys, getopt

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "n:a:")

	except getopt.GetoptError as e:
		print (str(e))
		print ("Usage: %s -n teste_name -action action" % sys.argv[0])
		sys.exit(2)

	for o, a in opts:
		if o == "-n":
			testReport = getLastTestReport(a)	

	fails = str(testReport['failCount'])
	passes = str(testReport['passCount'])

	print "passes: " + passes  + ", fails: " + fails 

def getLastTestReport(name):
	urlSufix = "/api/json"

	url = getTestUrl(name)
	runs = json.load(urllib2.urlopen(url + urlSufix))
	
	for build in runs['builds']:
		info = json.load(urllib2.urlopen(build['url'] + urlSufix))
		if info['building'] == False:
			break

	return json.load(urllib2.urlopen(info['url'] + "testReport" + urlSufix))

def getTestUrl(name):
	if name == "api":
		return "http://pagseguro.jenkins.srv.intranet/view/Testes%20de%20Integra%C3%A7%C3%A3o/job/TestesSeleniumApi"
	if name == "backend":
		return "http://pagseguro.jenkins.srv.intranet/view/Testes%20de%20Integra%C3%A7%C3%A3o/job/TestesSeleniumBackend"
	if name == "cadastro":
		return "http://pagseguro.jenkins.srv.intranet/view/Testes%20de%20Integra%C3%A7%C3%A3o/job/TestesSeleniumCadastro"
	if name == "checkout":
		return "http://pagseguro.jenkins.srv.intranet/view/Testes%20de%20Integra%C3%A7%C3%A3o/job/TestesSeleniumCheckout"
	if name == "gerenciador":
		return "http://pagseguro.jenkins.srv.intranet/view/Testes%20de%20Integra%C3%A7%C3%A3o/job/TestesSeleniumGerenciador"
	if name == "ibanking":
		return "http://pagseguro.jenkins.srv.intranet/view/Testes%20de%20Integra%C3%A7%C3%A3o/job/TestesSeleniumIbanking"
	else:
		sys.exit("Usage: -n teste_name -action action")

if __name__ == "__main__":
	main()
    