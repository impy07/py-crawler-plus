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

-s | --spider			Enable crawling
-l | --limit			Enable domain check, limiting the crawler within the staring domain
'''

FLAGS = ['-u','-t','-w','-v','-d','-h','-l','-s','--spider','--limit']
URL = ''
TAG_LIST = []
WORD_LIST=[]
VERBOSE = 0
DEPTH = 100
SPIDER = 0
LIMIT = 0
PREFIX = 'https://'

current_depth = 0
start_domain = ''
already_visited = []

def spider(url):
	global TAG_LIST
	global WORD_LIST
	global VERBOSE
	global DEPTH
	global current_depth
	global LIMIT
	global start_domain
	global already_visited
		
	response = search(url)
	
	if VERBOSE:
		print(f'Operating at depth: {current_depth}')
	
	if(response.ok):
		page = BS(response.content,'html.parser')
		
		links = page.find_all('a')
		if(current_depth <= DEPTH):
			if(len(links) > 0):
				current_depth +=1
			for link in links:
				if(VERBOSE):
					print(f'Link found: {link}')
				try:
					if '#' == link['href']:
						if(VERBOSE):
							print(f'No link in tag {link}, skipping')
							continue
					
					if urlparse(link['href']).netloc != start_domain and LIMIT:
						if(VERBOSE):
							print(f'Other domain in tag {link}, skipping')
							continue
					
					if 'http' not in link['href']:
						link['href'] = f'{PREFIX}{start_domain}{link["href"]}'
					
					if link['href'] not in already_visited:
						already_visited.append(link['href'])
						if VERBOSE:
							print(f'Added new link: {link["href"]}')
						spider(link['href'])
					else:
						if VERBOSE:
							print(f'Link Already Visited: {link["href"]}')
				except other:
					if(VERBOSE):
						print(f'Empty href for tag {link}, skipping')
						continue


def search(url,search=1):

	global TAG_LIST
	global WORD_LIST
	global VERBOSE
	found = 0
	word_len = len(WORD_LIST)
	
	if VERBOSE:
		print(f'Searching for URL {url}')
	
	try:
		response = requests.get(url)
	except:
		print(f'Error connecting to {url}')
		sys.exit(-1)
		
	if(response.ok):
		page = BS(response.content,'html.parser')
		print(f'Found URL: {url}')
		if(search):
			for tag in TAG_LIST:
				if VERBOSE:
					print(f'Results for tag {tag}:')
				for entry in page.find_all(tag):
					if(word_len == 0):
						print(entry)
					else:
						for word in WORD_LIST:
							if word in entry.text:
								found = 1
						if(found):
							print(entry)
							found = 0
				if VERBOSE:
					print('==========')
		else:
			print(page.prettify())
		print('')
			
	return response

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
	global start_domain
	global PREFIX
	
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
				
				if 'https' not in URL:
					PREFIX = 'http://'
			
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
		#Crawler
		start_domain = urlparse(URL).netloc
		spider(URL)
		
	else:
		#Single page research
		if(len(TAG_LIST) == 0):
			search(URL,0)
		else:
			search(URL)
	
	sys.exit(0)
	

if __name__ == '__main__':
	main()