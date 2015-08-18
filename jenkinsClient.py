#!/usr/bin/python
import urllib2, sys, getopt
from flask import Flask, json, jsonify
from collections import Counter

app = Flask(__name__)

@app.route('/info/<test_type>')
def get_general_info(test_type):
	test_report = get_last_test_report(test_type)

	fails = str(test_report['failCount'])
	passes = str(test_report['passCount'])

	return "passes: " + passes  + ", fails: " + fails

@app.route('/top/<test_type>')
def get_top_errors(test_type):
	test_report = get_last_test_report(test_type)
	counter = get_top_errors(test_report)

	response = {}
	return jsonify(counter.most_common(10))

def get_last_test_report(name):
	url_sufix = "/api/json"

	url = get_test_url(name)
	runs = json.load(urllib2.urlopen(url + url_sufix))
	
	for build in runs['builds']:
		info = json.load(urllib2.urlopen(build['url'] + url_sufix))
		if info['building'] == False:
			break

	return json.load(urllib2.urlopen(info['url'] + "testReport" + url_sufix))

def get_top_errors(test_report):
	counter = Counter()
	for class_name in test_report['suites']:
		for test in class_name['cases']:
			if test['status'] == "FAILED":
				counter[test['errorDetails']] += 1

	return counter

def get_test_url(name):
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
	app.run(debug=True)    