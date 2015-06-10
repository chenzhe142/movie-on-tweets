import json
import langid
import unicodedata

def main():
	with open('kingsman.txt') as data_file:
		data = json.load(data_file)

	result = []
	count = 0
	for tweet in data:
		# use langid module to filter a certain tweet by its language	
		classified = langid.classify(tweet['text'])	
		
		# if the classified result of tweet is English, save it to a single text file
		if classified[0] == 'en':
			if "http" not in tweet['text'] and "RT" not in tweet['text']:
				count += 1

				# parse unicode tweet['text'] to string
				# save it to a single text file
				parsed = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
				name = str(count) + ".txt"
				file = open(name, "w")
				file.write(parsed)
				file.close()
				
				print(parsed)
				print("===")

	print("------")
	print("count: " + str(count))

if __name__ == "__main__":
	main()