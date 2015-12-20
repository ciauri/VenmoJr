import unittest
from os import rename, path
import sqlite3
import datetime
from modules.db import Database

class TestDB(unittest.TestCase):

    testDbPath = path.join('tests','test.db')

    # Set up dummy test DB
    def setUp(self):
        self.connection = sqlite3.connect(self.testDbPath)
        self.cursor = self.connection.cursor()
        with open(path.join('db','schema.sql'), 'r') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()
        self.connection.close()

    def test_addUser(self):
        db = Database(self.testDbPath)
        self.assertFalse(db.addUser('stephen'))
        db.close()

    def test_addShortUser(self):
        db = Database(self.testDbPath)
        self.assertTrue(db.addUser('123'))
        db.close()

    def test_addLongUser(self):
        db = Database(self.testDbPath)
        self.assertTrue(db.addUser('1234567890123456'))
        db.close()

    def test_addDuplicateUser(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        self.assertTrue(db.addUser('stephen'))
        db.close()

    def test_addCard(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        self.assertFalse(db.addCard(23456789012345,1))
        db.close()

    def test_addDuplicateCard(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        db.addCard(23456789012345,1)
        self.assertTrue(db.addCard(23456789012345,1))
        db.close()

    def test_replaceCard(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        db.addCard(123456,1)
        self.assertTrue(db.addCard(654321,1))
        db.close()

    def test_addTransaction(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        db.addUser('billiam')
        db.addCard(123456,1)
        db.addCard(654321,2)
        self.assertFalse(db.addTransaction(1,2,100,'cool dude'))
        db.close()

    def test_getBalance(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        db.addUser('billiam')
        db.addCard(123456,1)
        db.addCard(654321,2)
        db.addTransaction(1,2,100,'cool dude')
        self.assertEqual(db.getBalance(2), 100)
        db.close()

    def test_getFeed(self):
        db = Database(self.testDbPath)
        db.addUser('stephen')
        db.addUser('billiam')
        db.addUser('this_guy')
        db.addCard(123456,1)
        db.addCard(654321,2)
        db.addTransaction(1,2,100,'cool dude')
        self.assertFalse(db.getFeed(3))
        db.close()


    def tearDown(self):
        rename('tests/test.db', 'tests/logs/TestDB{datetime}.db'.format(datetime=datetime.datetime.now()))



suite = unittest.TestLoader().loadTestsFromTestCase(TestDB)
unittest.TextTestRunner(verbosity=5).run(suite)
