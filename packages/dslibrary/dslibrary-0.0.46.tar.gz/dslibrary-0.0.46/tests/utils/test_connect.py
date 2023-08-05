import unittest
import pandas

from dslibrary.utils.connect import _process_params, dataframe_to_sql, db_conn_flavor, connect_psycopg2, \
    connect_to_database


class TestConnect(unittest.TestCase):
    def test__process_params(self):
        r = _process_params("mysql://u:p@host:1234/database", extra=1)
        assert r == {
            'host': 'host',
            'port': 1234,
            'database': 'database',
            'username': 'u',
            'password': 'p',
            'extra': 1
        }, r
        r = _process_params("xyz://u@host")
        assert r == {
            'host': 'host',
            'port': None,
            'database': '',
            'username': 'u',
            'password': ''
        }, r
        r = _process_params("sqlite:path/to/file")
        assert r == {
            'host': '',
            'port': None,
            'database': 'path/to/file',
            'username': '',
            'password': ''
        }, r
        r = _process_params("x://host/db", database="db2")
        assert r == {
            'host': 'host',
            'port': None,
            'database': 'db2',
            'username': '',
            'password': ''
        }, r

    def test_dataframe_to_sql(self):
        df = pandas.DataFrame({"x": [1, 2, 3], "y": [1.0, 2.0, 4.0], "z": ["one", "two", "three"]})
        sqls = list(dataframe_to_sql(df, "t1"))
        self.assertEqual(sqls, [
            ('DROP TABLE IF EXISTS t1', []),
            ('CREATE TABLE IF NOT EXISTS t1 (x INTEGER, y DOUBLE PRECISION, z VARCHAR(8))', []),
            ('INSERT INTO t1 (x, y, z) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)', [1, 1.0, 'one', 2, 2.0, 'two', 3, 4.0, 'three'])
        ])

    def test_db_conn_flavor(self):
        # artificially set property
        class A(object):
            _flavor = "xyz"
        self.assertEqual(db_conn_flavor(A()), "xyz")
        # name of class
        class MyPostGresDriver(object):
            pass
        self.assertEqual(db_conn_flavor(MyPostGresDriver()), "postgres")

    def test_sniff__pg(self):
        strategy = connect_to_database("postgres://u:p@host:1234/database", sniff_only=True)
        self.assertEqual(strategy.open_args, {'dsn': 'dbname=database host=host password=p port=1234 user=u'})
        import psycopg2
        self.assertIs(strategy.opener, psycopg2.connect)
