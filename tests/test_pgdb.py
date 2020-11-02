import unittest
from configparser import ConfigParser
import pypgdb
import psycopg2
import logging

logger = logging.getLogger("pgdb_unittest_log")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
)
logger.addHandler(ch)

#https://www.mysqltutorial.org/python-connecting-mysql-databases/


def read_db_config(filename='config.ini', section='pgsql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return " ".join((key + "=" + val) for (key, val) in db.items())


class PGDBTestCase(unittest.TestCase):
    def test_wrong_connection_string(self):
        logger.info("Test - test_wrong_connection_string")
        db = pypgdb.PGDB("test_string")
        with self.assertRaises(psycopg2.ProgrammingError):
            db.query("SELECT 1")

    def test_config_connection_string(self):
        logger.info("Test - test_config_connection_string")
        conn_string = read_db_config()
        db = pypgdb.PGDB(conn_string)
        self.assertEqual(db.query("SELECT 1 AS val")[0]["val"], 1)

    def test_open_close(self):
        logger.info("Test - test_open_close")
        conn_string = read_db_config()
        db = pypgdb.PGDB(conn_string)
        db.open()
        self.assertNotEqual(db._db, None)
        self.assertNotEqual(db._cursor, None)
        db.close()
        self.assertEqual(db._db, None)
        self.assertEqual(db._cursor, None)
        db.open()
        self.assertNotEqual(db._db, None)
        self.assertNotEqual(db._cursor, None)

    def test_insert_update_delete(self):
        logger.info("Test - test_insert_update_delete")
        conn_string = read_db_config()
        db = pypgdb.PGDB(conn_string)
        self.assertEqual(db.query("CREATE TEMPORARY TABLE pgdb_unit_test(value TEXT);"), False)

        self.assertEqual(db.query("INSERT INTO pgdb_unit_test SELECT generate_series(0, 30)::TEXT"), True)
        self.assertEqual(db.affected_rows, 31)

        self.assertEqual(db.query("UPDATE pgdb_unit_test SET value = 'unit_test' WHERE value::INTEGER < 10"), True)
        self.assertEqual(db.affected_rows, 10)

        self.assertEqual(db.query("DELETE FROM pgdb_unit_test WHERE length(value) = 2"), True)
        self.assertEqual(db.affected_rows, 21)

    def test_insert_update_delete_params(self):
        logger.info("Test - test_insert_update_delete_params")
        conn_string = read_db_config()
        db = pypgdb.PGDB(conn_string)

        self.assertEqual(db.query("CREATE TEMPORARY TABLE pgdb_unit_test(value TEXT, num INTEGER);"), False)

        values = [(x, x * "a") for x in range(0, 100)]

        for v in values:
            self.assertEqual(db.query("INSERT INTO pgdb_unit_test(value, num) VALUES(%s, %s)", (v[1], v[0])), 1)

        ret = db.query("SELECT * FROM pgdb_unit_test")
        self.assertEqual(len(ret), len(values))

        self.assertEqual(db.query("UPDATE pgdb_unit_test SET value = %s, num = %s WHERE num > %s AND num < %s",
                                  ("pdgb_test", -1, 9, 20)), True)
        self.assertEqual(db.affected_rows, 10)

        self.assertEqual(db.query("DELETE FROM pgdb_unit_test WHERE value = %s OR num > %s", ("pdgb_test", 98)), True)
        self.assertEqual(db.affected_rows, 11)


if __name__ == '__main__':
    unittest.main()
