import logging
import requests
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
from eye import search,colors,dump,licence,banner
                                             
def thedevilseye():
	start_time = datetime.now()
	parser = argparse.ArgumentParser(description=f'{colors.white}Darkweb .onion link(s) extracting tool{colors.reset}',epilog=f'{colors.white}thedevilseye extracts information (.onion links, descriptions) from the {colors.red}darkweb{colors.white} without requiring a Tor network. Developed by Richard Mwewa | https://about.me/{colors.green}rly0nheart{colors.reset}')
	parser.add_argument('-q','--query',metavar=f'{colors.white}search-query{colors.reset}', help=f'{colors.white}return results related to the search query{colors.reset}')
	parser.add_argument('-i','--i2p', help=f'{colors.white}switch to i2p network search{colors.reset}', action='store_true')
	parser.add_argument('--jailbait',help=f'{colors.white}Ahmia.fi self-help program;  {colors.red}The self-help program is primarily intended for people who are worried about their interest, thoughts, feelings or actions concerning children. {colors.white}Learn more at https://ahmia.fi/legal{colors.reset}',action='store_true')
	parser.add_argument('-d','--dump', metavar=f'{colors.white}path/to/file{colors.reset}', help=f'{colors.white}dump output to a specified file{colors.reset}')
	parser.add_argument('-v','--verbose',help=f'{colors.white}enable verbosity{colors.reset}',action='store_true')
	parser.add_argument('--release-tag',version=f'{colors.white}Hellfire#5 Released on 18th February 2022{colors.reset}',action='version')
	parser.add_argument('--licence','--license',help=f'show program\'s licen[cs]e and exit',action='store_true')
	args = parser.parse_args()
	
	print(banner.banner)
	if args.verbose:
		logging.basicConfig(format=f'{colors.white}* %(message)s{colors.reset}',level=logging.DEBUG)
	
	if args.jailbait:
		uri = f'https://ahmia.fi/search/?q=jailbait'
	elif args.i2p:
		uri = f'https://ahmia.fi/search/i2p/?q={args.query}'
	elif args.query:
		uri = f'https://ahmia.fi/search/?q={args.query}'
	elif args.licence:
		exit(licence.licence())
	else:
		exit(f'{colors.white}eye: use {colors.green}-h{colors.white} or {colors.green}--help{colors.white} to show help message.{colors.reset}')
		
	while True:
		try:
			search.search(args,uri,start_time)
			break
			
		except KeyboardInterrupt:
		    if args.verbose:
		        logging.info(f'{colors.white}Process interrupted with {colors.red}Ctrl{colors.white}+{colors.red}C{colors.reset}')
		        break
		    break
		    
		except Exception as e:
		    if args.verbose:
		        logging.error(f'{colors.white}An error occured: {colors.red}{e}{colors.reset}')
	
	if args.verbose:
	    logging.info(f'{colors.white}Finished in {colors.green}{datetime.now()-start_time}{colors.white} seconds.{colors.reset}')
	exit()