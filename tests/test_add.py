import unittest
from os import rename
import sqlite3
import datetime
from modules.add import Add
from modules.user import User

class TestAdd(unittest.TestCase):

    testDbPath = 'tests/test.db'

    # Set up dummy test DB
    def setUp(self):
        self.connection = sqlite3.connect(self.testDbPath)
        self.cursor = self.connection.cursor()
        with open('db/schema.sql', 'r') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()
        self.connection.close()
        User(self.testDbPath, 'stephen')
        User(self.testDbPath, 'james')

    def test_addCard(self):
        u = Add(self.testDbPath, 'stephen', '4111111111111111')
        self.assertTrue(u.success)

    def test_addBadCard(self):
        u = Add(self.testDbPath, 'stephen', '1234567890123456')
        self.assertFalse(u.success)

    def test_addAnotherCard(self):
        Add(self.testDbPath, 'stephen', '5454545454545454')
        v = Add(self.testDbPath, 'stephen', '4111111111111111')
        self.assertFalse(v.success)

    def test_addDupCard(self):
        u = Add(self.testDbPath, 'stephen', '5454545454545454')
        u = Add(self.testDbPath, 'james', '5454545454545454')
        self.assertFalse(u.success)

    def test_addBadUser(self):
        u = Add(self.testDbPath, 'thisguy', '5454545454545454')
        self.assertFalse(u.success)

    def test_addShortCard(self):
        u = Add(self.testDbPath, 'stephen', '123')
        self.assertFalse(u.success)

    def test_addLongCard(self):
        u = Add(self.testDbPath, 'stephen', '12345678901234567890123456')
        self.assertFalse(u.success)



    def tearDown(self):
        rename('tests/test.db', 'tests/logs/TestAdd{datetime}.db'.format(datetime=datetime.datetime.now()))



suite = unittest.TestLoader().loadTestsFromTestCase(TestAdd)
unittest.TextTestRunner(verbosity=5).run(suite)
