import unittest
from os import rename
import sqlite3
import datetime
from modules.user import User

class TestUser(unittest.TestCase):

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

    def test_addUser(self):
        u = User(self.testDbPath, 'stephen')
        self.assertFalse(u.success)

    def test_addDuplicateUser(self):
        u = User(self.testDbPath, 'stephen')
        u = User(self.testDbPath, 'stephen')
        self.assertTrue(u.success)

    def test_addShortUser(self):
        u = User(self.testDbPath, 'k')
        self.assertTrue(u.success)

    def test_addLongUser(self):
        u = User(self.testDbPath, '1234567890123456')
        self.assertTrue(u.success)

    def test_addInvalidUser(self):
        u = User(self.testDbPath, '!@#$^*(%)lolk')
        self.assertTrue(u.success)




    def tearDown(self):
        rename('tests/test.db', 'tests/logs/TestUser_{datetime}.db'.format(datetime=datetime.datetime.now()))



suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
unittest.TextTestRunner(verbosity=5).run(suite)
