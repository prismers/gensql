import unittest

from sqlgen.utilities.utility import dropPart


class MyTestCase(unittest.TestCase):

    def test_drop(self):
        s = 'SELECT a FROM t WHERE 1;'
        assert dropPart(s, 'WHERE') == ('SELECT a FROM t ;', ' 1;')

        s = 'SELECT a FROM t1 JOIN t2 ON 1;'
        assert dropPart(s, 'ON') == ('SELECT a FROM t1 JOIN t2 ;', ' 1;')

        s = 'SELECT a FROM t1 JOIN t2 ON 1 WHERE 1;'
        assert dropPart(s, 'ON') == ('SELECT a FROM t1 JOIN t2 ;', ' 1 WHERE 1;')

    def test_mutation(self):
        import mysql.connector
        try:
            cnx = mysql.connector.connect("")
            s = "SELECT t1.`col_double_key_signed` , t2.`col_float_undef_signed` FROM table_10_latin1_undef AS t1 " \
                "INNER JOIN table_10_latin1_4 AS t2 ON ( CONVERT( NULL, SIGNED ) ) / 'o';"
        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
