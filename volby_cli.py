import requests
from bs4 import BeautifulSoup
import click
import csv



nuts_url = 'https://volby.cz/opendata/ps2017nss/PS_nuts.htm'

okres_url = 'https://volby.cz/pls/ps2017nss/vysledky_okres?nuts=CZ0100'

def get_nuts():
	r = requests.get(nuts_url)
	r.encoding = 'windows-1250'
	soup = BeautifulSoup(r.text, 'lxml')
	for row in soup.find_all('tr'):
		cols = row.find_all('td',attrs={'class':'xl678667'})
		if cols:
			code = cols[0].text
			name = cols[1].text
			print(code, name)
			yield code
def get_obce(code):
	r = requests.get(f"https://volby.cz/pls/ps2017nss/vysledky_okres?nuts={code}")
	soup = BeautifulSoup(r.text, 'lxml')
	for obec in soup.find_all('obec'):
		yield code,obec['naz_obec']


def generate_csv(filename):

	with open(filename, 'w', newline='') as csvfile:
		fieldnames = ['code', 'obec_name']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for code in get_nuts():
			for code, obec_name in get_obce(code):
				writer.writerow({'code': code, 'obec_name': obec_name})

def read_csv(filename):
	with open(filename, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		list_out = [row for row in reader]
	return list_out
	
#this needs to run at least once
#generate_csv('names.csv')
obce_list = read_csv('names.csv')
@click.command()
@click.option('--name', prompt=True)
def volby_cli(name):
    click.echo(f"Hello {name}!")


if __name__ == '__main__':
    volby_cli()