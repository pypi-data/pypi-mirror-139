import requests
from eye import colors,dump
from bs4 import BeautifulSoup
from datetime import datetime

# Searching on ahmia
def search(args,uri,start_time):
	request = requests.get(uri)
	soup = BeautifulSoup(request.text, 'html.parser')
	
	if soup.ol is None:
	    if args.verbose:
	        logging.warning(f'{white}No results found for {args.query}. Try a different search.{reset}')
	        exit()
	else:
	    a_string = f'{args.query}'
	    if args.verbose:
	        if args.jailbait:
	        	a_string = 'JAILBAIT'
	        print(f'\n\t{a_string} — thedevilseye | ',start_time.strftime('%A %d %B %Y, %I:%M:%S%p'))
	    print(soup.ol.get_text())
	    
	if args.dump:
		dump.dump(args,soup)