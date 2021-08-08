# prusa_volby

CLI tool for graphing voting results from volby.cz

```
Usage: volby_cli.py [OPTIONS]

  Tool to get live colorful voting results for a specified obec. Data are
  downloaded from https://volby.cz each time you run this.

Options:
  --obec TEXT                     Name of the obec you are intrested in, if
                                  ambiguous interactive choice will be shown.
  --refresh / --no-refresh        Some static data are stored in the names.csv
                                  and parties.csv files, use --refresh to
                                  recreate those files.
  --sort-results / --no-sort-results
                                  Use --no-sort-results if you do not want the
                                  results sorted by percentage of votes
                                  recieved.
  --help                          Show this message and exit.

```

## Instalation of dependencies

Use the following command to install the required packages


`python3 -m pip install -r requirements.txt`

## Example usage

```
python3 volby_cli.py --help
python3 volby_cli.py
python3 volby_cli.py --obec='Praha 2'
python3 volby_cli.py --obec='Zvole'
python3 volby_cli.py --obec='Praha 2' --no-sort-results
python3 volby_cli.py --obec='Praha 1' --refresh
```