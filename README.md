# gensql
Python package to generate random simple ddls and queries with a brute-force approach

## Description

### Summary
This is a standalone database and query generation tool.
* Features: table, data and query generation
* Language: `Python 3`
* Dialects: mainly `MySQL`

### Usage
You could see the tests unders `./sqlgen/test` for examples. Generally, we have:
* A database generator: `./sqlgen/gentable`
* A SQL generator: `./sqlgen/gensql`
* A general driver to connect different databases `driver.py`
````Bash
usage: driver.py [-h] [-D {mysql,mariadb,tidb,postgres,sqlite,timescale}]
                 [-H HOST] [-P PORT] [-u USER] [-p PASSWORD] [-d DATABASE]

optional arguments:
  -h, --help            show this help message and exit
  -D {mysql,mariadb,tidb,postgres,sqlite,timescale}, --driver {mysql,mariadb,tidb,postgres,sqlite,timescale}
                        database server
  -H HOST, --host HOST  host
  -P PORT, --port PORT  port
  -u USER, --user USER  the user to connect the database
  -p PASSWORD, --password PASSWORD
                        password
  -d DATABASE, --database DATABASE
                        use the given database. Need file path if connecting
                        to sqlite.
````
## Tests
````Bash
python3 -m unittest discover
````

## Dependencies
* Python (>= 3.7))
* moz-sql-parser (dev branch only)
    *  For MySQL, it is better to use [customized version](https://github.com/zhangysh1995/moz-sql-parser)
* Database drivers
    *  MySQL: `mysql-connector-python` (>= 8.0.19)
    
## Contributions
If you want  to improve this tool, you could start from the following lists:
* Refactor
    *  Hard-coded generation rules in `./sqlgen/gen*`
* Unit tests
    *  Check `./sqlgen/test`