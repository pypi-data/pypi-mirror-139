#!/usr/bin/env python3

import logging
import argparse
import requests
from datetime import datetime
from occli import search,colors,banner,licence

def occli():
	# Parsing command line arguments
	parser = argparse.ArgumentParser(description=f"{colors.white}OpenCorporates Command Line Interface [{colors.red}Unofficial{colors.white}]{colors.reset}",epilog=f"{colors.green}OpenCorporates.com{colors.white} is a website that shares data on corporations under the copyleft Open Database License. Developed by {colors.green}Richard Mwewa{colors.white} | https://about.me/{colors.green}rly0nheart{colors.reset}")
	parser.add_argument('-q','--query',metavar=f'{colors.white}company-name{colors.reset}')
	parser.add_argument("-d","--dump",help=f"{colors.white}dump output to a specified file{colors.reset}",metavar=f"{colors.white}path/to/file{colors.reset}")
	parser.add_argument("-v","--verbose",help=f"{colors.white}run occli in verbose mode{colors.reset}",action="store_true")
	parser.add_argument("--version",version=f"{colors.white}v0.3.4 Released on 16th February 2022 {colors.reset}",action="version")
	parser.add_argument('--licence','--license',help=f'show program\'s licen(cs)e and exit',action='store_true')
	args = parser.parse_args()

	start_time = datetime.now()
	api = f"https://api.opencorporates.com/v0.4.8/"
	print(banner.banner)
	if args.verbose:
		logging.basicConfig(format=f'{colors.white}* %(message)s{colors.reset}',level=logging.DEBUG)
		
	while True:
		try:
			if args.query:
				search.search(args,api)
				break
			elif args.licence:
				exit(licence.content)
			else:
				exit(f"{colors.white}occli: use {colors.green}-h{colors.white} or {colors.green}--help{colors.white} to show help message.{colors.reset}")
				
		except KeyboardInterrupt:
		    if args.verbose:
		    	print('\n')
		    	logging.critical(f"{colors.white}Process interrupted with {colors.red}Ctrl{colors.white}+{colors.red}C{colors.reset}")
		    	break
		    break
				
		except IndexError:
		    break
		    
		except Exception as e:
		    if args.verbose:
		    	logging.warning(f"{colors.white}An error occured: {colors.red}{e}{colors.reset}")
		    
	if args.verbose:
		logging.info(f"{colors.white}Finished in {colors.green}{datetime.now()-start_time}{colors.white} seconds.{colors.reset}")