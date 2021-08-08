import requests
from bs4 import BeautifulSoup
import click
import csv
from colorama import Fore, Back, Style


def get_nuts():
	# TODO: handle the unhappy path 
	nuts_url = 'https://volby.cz/opendata/ps2017nss/PS_nuts.htm'
	r = requests.get(nuts_url)
	r.encoding = 'windows-1250'
	soup = BeautifulSoup(r.text, 'lxml')
	for row in soup.find_all('tr'):
		cols = row.find_all('td',attrs={'class':'xl678667'})
		if cols:
			code = cols[0].text
			name = cols[1].text
			print(code, name)
			yield code, name
			
def get_obce(code):
	# TODO: handle the unhappy path 
	r = requests.get(f"https://volby.cz/pls/ps2017nss/vysledky_okres?nuts={code}")
	soup = BeautifulSoup(r.text, 'lxml')
	for obec in soup.find_all('obec'):
		yield code,obec['naz_obec']

def get_party_names(filename):
	# TODO: handle the unhappy path 
	url = 'https://volby.cz/pls/ps2017nss/vysledky'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')
	with open(filename, 'w', newline='') as csvfile:
		fieldnames = ['code', 'strana_name']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		kraj = soup.find('kraj')
		for strana in kraj.find_all('strana'):
			writer.writerow({'code':strana['kstrana'], 'strana_name':strana['naz_str']})


def generate_csv(filename):

	with open(filename, 'w', newline='') as csvfile:
		fieldnames = ['code', 'okres_name','obec_name']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for nuts_code, name in get_nuts():
			for code, obec_name in get_obce(nuts_code):
				writer.writerow({'code': code, 'okres_name': name,'obec_name': obec_name})

def read_csv(filename):
	with open(filename, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		list_out = [row for row in reader]
	return list_out

def read_party_names(filename):
	with open(filename, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		list_out = [row for row in reader]
	return list_out




def get_okres_results(okres_code, obec_name):
	# TODO: handle the unhappy path 
	okres_url = f'https://volby.cz/pls/ps2017nss/vysledky_okres?nuts={okres_code}'
	r = requests.get(okres_url)
	soup = BeautifulSoup(r.text, 'lxml')
	obec =soup.find('obec', attrs = {'naz_obec': obec_name})
	return [ (x['kstrana'], x['proc_hlasu']) for x in obec.find_all('hlasy_strana')]


def transform_results(results, parties, sort_results=True):
	# TODO: use pandas or smth 
	transformed = []
	for r in results:
		name =  [x['strana_name'] for x in parties if x['code']==r[0]][0]
		percentage = float(r[1])

		transformed.append({"name":name, "percentage": percentage, "code": int(r[0])})
	if sort_results:
 		newlist = sorted(transformed, key=lambda k: k['percentage'], reverse=True)
 		return newlist 
	return transformed



def graph_results(results):
	fat_tick = "▇"
	colors = [Fore.GREEN, Fore.YELLOW, Fore.WHITE, Fore.BLUE, Fore.RED, Fore.CYAN, Fore.MAGENTA]
	for r in results:
		bar = fat_tick + fat_tick * int(r['percentage'])
		if r['percentage'] == 0.0:
			bar = ''
		color = colors[r['code'] % len(colors)]
		print(f"{color} {bar}{Style.RESET_ALL} {r['name']} {str(r['percentage'])}%")

	


@click.command()
@click.option('--obec', prompt=True)
@click.option('--refresh/--no-refresh', default=False)
@click.option('--sort-results/--no-sort-results', default=True)
def volby_cli(obec, refresh, sort_results):
	if refresh:

		generate_csv('names.csv')
		get_party_names('parties.csv')
	try:
		obce_list = read_csv('names.csv')
		parties = read_party_names('parties.csv')
	except FileNotFoundError:
		click.echo('Obce csv file not found use --refresh first')
		exit(1)
	click.echo(f"Searching {obec}!")
	matches = [x for x in obce_list if x['obec_name']==obec]

	if len(matches) == 0:
		click.echo(f"Found no obec matching {obec}!")
		exit(1)
	elif len(matches) == 1:
		click.echo("One obec found!")
		results = get_okres_results(matches[0]['code'],matches[0]['obec_name'])
	elif len(matches) > 1:
		click.echo(f'Found multiple obec matching the name {obec}!')
		for o in matches:
			print(f"{o['code']}: {o['okres_name']} - {o['obec_name']}")
		code = click.prompt('Select one code',type=click.Choice([o['code'] for o in matches]))
		matches = [x for x in matches if x['code']==code]
		results = get_okres_results(matches[0]['code'],matches[0]['obec_name'])


	trans = transform_results(results, parties, sort_results)
	graph_results(trans)


if __name__ == '__main__':
	 volby_cli()