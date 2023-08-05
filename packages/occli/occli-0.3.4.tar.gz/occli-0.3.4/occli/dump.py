import logging
from occli import colors

# Writing results to a file
def write(args,data,number,response):
    with open(args.dump, "a") as file:
        file.write(f"\n\n{response['results']['companies'][number]['company']['name']}\n")
        for key, value in data.items():
        	file.write(f" ├─ {key}: {value}\n")
        file.close()
        	
    if args.verbose:
        logging.info(f"{colors.white}Output written to {colors.green}{args.dump}{colors.reset}")