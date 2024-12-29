# pscachier
PeopleSoft Cache Tool

```
$ pscachier --help
Usage: pscachier [OPTIONS] COMMAND [ARGS]...

  PeopleSoft Cache Tool

Options:
  --help  Show this message and exit.

Commands:
  app  Working with Application Server cache
```

# Usage

## app

```
$ pscachier app --help
Usage: pscachier app [OPTIONS] COMMAND [ARGS]...

  Working with Application Server cache

Options:
  --help  Show this message and exit.

Commands:
  copycache  Copy generated cache to PSAPPSRVs
  loadcache  Run the LOADCACHE program to generate cache
```

### loadcache

```
$ pscachier app loadcache --help
Usage: pscachier app loadcache [OPTIONS]

  Run the LOADCACHE program to generate cache

Options:
  -db, --database TEXT     Database  [required]
  -o, --options-file TEXT  Location to store temporary options file for AE
                           [default: /home/psadm2/psae.options]
  -sd, --ps-servdir TEXT   Directory used to store generated cache  [required]
  -r, --rebase             Delete current generated cache to rebase
  --help                   Show this message and exit
```

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PS_HOME/python/lib
export PSC_USER="PS"
export PSC_PASS="PS"
export PSC_CONN_ID="people"
export PSC_CONN_PW="peop1e"

pscachier app loadcache loadcache --database FSCMDB --ps-servdir /home/psadm2/pscache
```

### copycache

```
$ pscachier app copycache --help
Usage: pscachier app copycache [OPTIONS]

  Copy generated cache to PSAPPSRVs

Options:
  -d, --domain TEXT        App server domain name  [required]
  -sd, --ps-servdir TEXT   Directory used to store generated cache  [required]
  -r, --rebase             Rebase cache
  --help                   Show this message and exit
```

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PS_HOME/python/lib

pscachier app copycache --domain APPDOM --ps-servdir /home/psadm2/pscache
```

# Installing
```
cd pscachier
pip install --user .
```

# Setting up for development
```
pip install virtualenv 

cd psst
virtualenv -p python3 venv
. venv/bin/activate

pip install --editable .
```
