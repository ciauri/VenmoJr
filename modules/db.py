from os import path
import sqlite3
import logging

logging.basicConfig(filename='logs/log.txt', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
dbLog = logging.getLogger("venmojr.db")

class Database:

    def __init__(self, path='db/baby.db'):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute('pragma foreign_keys=ON')
        # If DB doesn't exist, create one
        if not self.__schemaIsValid():
            dbLog.info("DB is empty. Importing schema.")
            self.__createNew()


    def addUser(self, username):
        try:
            sql = "insert into user(username) values(?)"
            dbLog.info(sql.replace('?',username))
            self.cursor.execute(sql, (username,))
            self.connection.commit()
            return 0
        except sqlite3.IntegrityError as e:
            dbLog.error(e)
            dbLog.error("Cannot create user {uname} because the username is already in use".format(uname=username))
            return 1

    def addCard(self, number, uid):
        try:

            # Check if user already has a card on file
            if self.getCID(uid=uid):
                dbLog.error("User already has card associated with account")
                print "ERROR: User already has a card associated with their account."
                return 1
            else:
                sql_insert = "insert into cc(number, uid) values(?,?)"
                sql_update = "update user set card = ? where uid = ?"

                dbLog.info(sql_insert.replace('?',str(number),1).replace('?',str(uid),1))
                self.cursor.execute(sql_insert, (number, uid))

                cardID = self.getCID(card=number)
                dbLog.info(sql_update.replace('?',str(cardID),1).replace('?',str(uid),1))
                self.cursor.execute(sql_update, (cardID,uid))

                self.connection.commit()
                return 0
        except sqlite3.IntegrityError:
            dbLog.error("Card {card} already in use".format(card=number))
            print "This card is already being used. A card may only be associated with one user account."
            return 1

    def addTransaction(self, srcID, dstID, amount, note=None):
        # Assuming infinite credit, I suppose!
        sql_insert = "insert into trans(src, dst, amount, note) values(?,?,?,?)"
        sql_update = "update user set balance = balance + ? where uid = ?"

        dbLog.info(sql_insert.replace('?',str(srcID),1).replace('?',str(dstID),1).replace('?',str(amount),1).replace('?',str(note),1))
        self.cursor.execute(sql_insert, (srcID, dstID, amount, note))

        dbLog.info(sql_update.replace('?',str(amount),1).replace('?',str(dstID),1))
        self.cursor.execute(sql_update, (amount, dstID))

        self.connection.commit()
        return 0

    def getBalance(self, uid):
        self.cursor.execute("select balance from user where uid == ?", (uid,))
        return self.cursor.fetchone()[0]

    def getFeed(self, uid):
        self.cursor.execute("select * from trans where src==? or dst==?", (uid,uid))
        try:
            return self.cursor.fetchall()
        except:
            return 0

    # User ID
    def getUID(self, username):
        self.cursor.execute("select uid from user where username == ?", (username,))
        try:
            return self.cursor.fetchone()[0]
        except:
            return 0

    # User name
    def getUname(self, uid):
        self.cursor.execute("select username from user where uid == ?", (uid,))
        try:
            return self.cursor.fetchone()[0]
        except:
            return 0


    # Card ID
    def getCID(self, card=0, uid=0):
        if card != 0:
            self.cursor.execute("select cid from cc where number == ?", (card,))
            try:
                return self.cursor.fetchone()[0]
            except:
                return 0
        elif uid != 0:
            self.cursor.execute("select cid from cc where uid == ?", (uid,))
            try:
                return self.cursor.fetchone()[0]
            except:
                return 0

    def __schemaIsValid(self):
        try:
            self.cursor.execute("select * from user")
            self.cursor.fetchone()[0]
            return True
        except sqlite3.OperationalError:
            return False

    def __createNew(self):
        with open(path.join('db','schema.sql'), 'r') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()





    def close(self):
        return self.connection.close()




