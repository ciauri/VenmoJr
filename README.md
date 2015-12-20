#Usage
##Requirements:

    python 2.7
I’m pretty sure 2.7 comes shipped with the sqlite3 package.

This code is pretty straightforward. To run it, simply pass the ‘venmojr.py’ file into a python 2.7 interpreter from within the venmojr directory like so:

    python venmojr.py
If you would like to pass in an inputfile for batch processes, just add it to the 2nd parameter like so:

    python venmojr.py path/to/inputfile

If you would like to run a full unit test, feel free to run runTests.sh. If you’re on a windows box, run this within the exploded directory:

    python -m unittest discover
#Design Decisions
As with most projects, this changed forms quite a few times during development. In an attempt to be as OO as possible, I ended up making modules for each function of the ‘engine’ if you can even call it that. However, most of the OO paradigms aren’t even really used here. Especially in such a minimal transaction-based system, I didn’t really see a reason to make use of inheritance, static methods, or anything specifically ‘classy’. Everything is pretty procedural here.

It has a persistent SQLite database that will auto-load if empty. For testing purposes, I implemented the ability to act on any database you want at any time by using a naive ‘session’ variable within the simple interpreter. This way, I can create any test DB I want while not interfering with the ‘live’ db.

The way I designed this app, it would be easy for anyone to add on a module so long as they follow the rules and add it to the ‘validCommands’ array. I’m happy with how simple the interpreter ended up being.
