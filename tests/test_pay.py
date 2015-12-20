import unittest
from os import rename
import sqlite3
import datetime
from modules.add import Add
from modules.user import User
from modules.pay import Pay

class TestPay(unittest.TestCase):

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
        Add(self.testDbPath, 'stephen', '5454545454545454')

    def test_pay(self):
        p = Pay(self.testDbPath, 'stephen','james', '$20.00', 'waddapdude')
        self.assertTrue(p.success)

    def test_payNoCc(self):
        p = Pay(self.testDbPath, 'james','stephen', '$20.00', 'waddapdude')
        self.assertFalse(p.success)

    def test_paySelf(self):
        p = Pay(self.testDbPath, 'stephen','stephen', '$20.00', 'waddapdude')
        self.assertFalse(p.success)

    def test_payInvalidSourceUser(self):
        p = Pay(self.testDbPath, 'lolthisguy','stephen', '$20.00', 'waddapdude')
        self.assertFalse(p.success)

    def test_payInvalidDestinationUser(self):
        p = Pay(self.testDbPath, 'stephen','skippidy-doo-dah', '$20.00', 'waddapdude')
        self.assertFalse(p.success)

    def test_payInvalidAmountSyntax(self):
        p = Pay(self.testDbPath, 'stephen','james', '20.00', 'waddapdude')
        q = Pay(self.testDbPath, 'stephen','james', '$.00', 'waddapdude')
        r = Pay(self.testDbPath, 'stephen','james', '0', 'waddapdude')
        s = Pay(self.testDbPath, 'stephen','james', '-1', 'waddapdude')
        t = Pay(self.testDbPath, 'stephen','james', '20.20.20', 'waddapdude')
        self.assertFalse(p.success and q.success and r.success and s.success and t.success)


    def tearDown(self):
        rename('tests/test.db', 'tests/logs/TestPay{datetime}.db'.format(datetime=datetime.datetime.now()))



suite = unittest.TestLoader().loadTestsFromTestCase(TestPay)
unittest.TextTestRunner(verbosity=5).run(suite)
