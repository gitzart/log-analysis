# Logs Analysis
A reporting tool to analyze the web server logs of a newspaper site.

### Getting started

Unzip the `newsdata` zip file. Install dependencies
```
$ pip install -r requirements.txt
```

Import the schema and load the data
```
$ psql -d database -f newsdata.sql
```

Export database url
```
$ export DATABASE_URL=postgres://user:pass@host:port/database
```

Run `$ python report.py`
