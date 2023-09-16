import sys,os,requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

help_str = f'''Usage: {sys.argv[0]} [-v] -u <URL> -t <TAG_LIST>
-u				URL
-t				TAG_LIST: list of tag to search
-w				WORD_LIST: list of words to search
-v | --verbose	VERBOSE: more printout
-h | --help		Display help message
-d				DEPTH: limits the depth of the research, default is set to 100

--spider			Enable crawling
--limit			Enable domain check, limiting the crawler within the staring domain
'''

FLAGS = ['-u','-t','-w','-v','-d','-h','--spider','--limit']
URL = ''
TAG_LIST = []
WORD_LIST=[]
VERBOSE = 0
DEPTH = 100
SPIDER = 0
LIMIT = 0

current_depth = 0

def search(url,search=1):
	global TAG_LIST
	global WORD_LIST
	global VERBOSE
	
	page = requests.get(URL)
	page = BS(page.content,'html.parser')
	
	if(search):
		for tag in TAG_LIST:
			print(f'Result for tag {tag}')
			for entry in page.find_all(tag):
				print(entry)
			print('==========')
		
		for word in WORD_LIST:
			print(f'Result for word {word}')
			for entry in page.find_all(text=word):
				print(entry)
			print('==========')
	else:
		print(page.prettify())

def main():
	
	global FLAGS
	global URL
	global TAG_LIST
	global WORD_LIST
	global VERBOSE
	global DEPTH
	global SPIDER
	global LIMIT
	global current_depth
	global help_str
	
	params = sys.argv[1::]
	length = len(params)
	ctr = 0
	
	if length == 0:
		print(help_str)
		sys.exit(-1)
	while(ctr < length):
		match params[ctr]:
			case '-u':
				if(ctr+1>=length or params[ctr+1] in FLAGS):
					print('No URL provided, exit')
					sys.exit(-1)
				URL = params[ctr+1]
				if(VERBOSE):
					print('URL detected: '+URL)
				if 'http' not in URL:
					print('Incomplete URL format, exit')
					sys.exit(-1)
			
			case '-t':
				if not (ctr+1>=length or params[ctr+1] in FLAGS):
					TAG_LIST.extend(params[ctr+1].split(','))
					if(VERBOSE):
						print(f'TAG_LIST in use: {TAG_LIST}')
					
			case '-w':
				if not (ctr+1>=length or params[ctr+1] in FLAGS):
					WORD_LIST.extend(params[ctr+1].split(','))
					if(VERBOSE):
						print(f'WORD_LIST in use: {WORD_LIST}')
			
			case '-v' | '--verbose':
				print('Verbose Mode Enabled')
				VERBOSE = 1
				ctr-=1
				
			case '-h' | '--help':
				print(help_str)
				sys.exit(0)
				
			case '-d':
				if not (ctr+1>=length or params[ctr+1] in FLAGS):
					DEPTH = int(params[ctr+1])
					if(VERBOSE):
						print('Depth set to: '+DEPTH)
					
			case '--spider' | '-s':
				if(VERBOSE):
					print('Spider Mode Enabled')
				SPIDER = 1
				ctr-=1
				
			case '--limit' | '-l':
				if(VERBOSE):
					print('Search limited to starting domain')
				LIMIT = 1
				ctr-=1
				
			case other:
				print(f'Invalid argument {params[ctr]}, exit')
				sys.exit(-1)
		ctr+=2
	
	if(SPIDER):
		#TODO: Crawler
		pass
	else:
		#TODO: Single page research
		if(len(TAG_LIST) == 0 and len(WORD_LIST) == 0):
			search(URL,0)
		else:
			search(URL)
	
	sys.exit(0)
	

if __name__ == '__main__':
	main()