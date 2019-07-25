import requests
from stem import Signal
from stem.control import Controller



def startPrivateProxy():
	with Controller.from_port(port=9051) as controller:
		PASS_WORD = "andyanh@diginet#123"
		controller.authenticate(PASS_WORD)
		controller.signal(Signal.NEWNYM)
		 

	proxies = {
		
		"http:": "http://127.0.0.1:8118"
	}

	return proxies
