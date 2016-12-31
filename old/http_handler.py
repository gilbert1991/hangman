import requests
import json

def downloadJsonFile(url, dest):
	response = requests.get(url, stream=True)

	if response.status_code != 200:
		print "Http Error: %s, %d" % (url, response.status_code)
	else:
		with open(dest, 'wb') as f:
			json.dump(response.json(), f)


if __name__ == '__main__':
	response = requests.get("https://gist.githubusercontent.com/lydell/259ab9f2ddaa1a64e6bd/raw/6e385151fd5de34e924a1e65f78d152c86afff76/bigrams-all.json")
	dic = response.json()
	print dic[2]


