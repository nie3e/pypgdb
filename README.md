# pypgdb
pgdb is a simple wrapper around psycopg2 python library to simplify its usage.

  - Connection is established before the first query or manually by calling ```open``` function.
  - You can close connection using ```close``` function or by deleting PGDB object.
  - Use logger object for more output information ```pgdb.logger.setLevel(logging.INFO)```

### Typical usage example
```py
from pypgdb import pgdb
import logging
db = pgdb.PGDB("host=127.0.0.1 dbname=my_db port=5432 user=myUser password=myPassword")
pgdb.logger.setLevel(logging.INFO)
res = db.query("SELECT 'hello world'::TEXT, NOW()")
```
### Installation
pypgdb requires psycopg2 to run.

pip installation:
```sh
pip install pypgdb
```

Install from source:
```sh
python setup.py bdist_wheel
pip install dist\pypgdb-VERSION-py3-none-any.whl
```