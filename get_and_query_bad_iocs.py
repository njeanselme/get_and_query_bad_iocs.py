import requests
import json
import dns
import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['127.0.0.1'] # Assuming BloxOne endpoint is setup and enabled

headers = {
  'Authorization': 'Token XXXXXXXXX_PASTE_YOUR_CSP_Token_Here'
}

url = "https://csp.infoblox.com/tide/api/data/threats?type=host&class=apt&class=bot&class=intrusionattempt&class=malwarec2&class=malwarec2dga&class=malwaredownload&class=webappattack&threat_level=100&confidence=100&data_format=json&risk_score_rating=Critical&rlimit=100"
payload={}

response = requests.request("GET", url, headers=headers, data=payload)

if response.text:
	try:
		r_json=json.loads(response.text)
	except:
		print(response.text)
		raise Exception("Unable to load into a json format")
	
	for ioc in r_json["threat"]:
		print(ioc["host"])
		try:
			result = dns.resolver.query(ioc["host"], 'A')
			for ipval in result:
				print('IP', ipval.to_text())			
		except:
			pass
