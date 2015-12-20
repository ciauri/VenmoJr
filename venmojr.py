import sys
from os import path
from modules.user import User
from modules.pay import Pay
from modules.add import Add
from modules.feed import Feed
from modules.balance import Balance

class SimpleInterpreter:

    validCommands = {'user':User,
                     'add':Add, 'pay':Pay,'feed':Feed, 'balance':Balance}

    def __init__(self, db=path.join('db','baby.db')):
        self.dbPath = db



    def printUsage(self):
        print "\nValid commands are as follows:\n"
        for c in self.validCommands:
            print c
        print"\nFor additional usage information, type a command with no arguments"

    def printLogo(self):
        print """
                 **********************************
                 *      Welcome to VenmoJR!       *
                 *                                *
                 *      By: Stephen Ciauri        *
                 **********************************"""

    def mainLoop(self):
        command = ''
        self.printLogo()
        self.printUsage()
        while(command != "exit"):
            userinput = raw_input("> ")
            command = userinput.split()[0]
            self.commandProcessor(userinput)

    def commandProcessor(self, userinput):
            command = userinput.split()[0]
            args = userinput.split()[1:]
            args.insert(0,self.dbPath)
            if command in self.validCommands.keys():
                if args:
                    self.validCommands[command](*args)
                else:
                    self.validCommands[command]()
            else:
                if command != 'exit':
                    print "Invalid command"

    def batchProcess(self, path):
        with open(path, 'r') as f:
            for line in f:
                self.commandProcessor(line)




""" Don't really need this here. Can sanitize input per-module.

    def checkAlphanumeric(self, userinput):
        if re.match('^[\w+\s\$?\.?\-*\'*\"*\@*\%*\#*\]+$', userinput):
            return userinput
        else:
            return 0

"""



if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args == 1:
        venmojr = SimpleInterpreter()
        venmojr.mainLoop()
    elif num_args == 2:
        venmojr = SimpleInterpreter()
        venmojr.batchProcess(sys.argv[1])
    else:
        print "usage: python venmojr.py [path-to-input-file]"


