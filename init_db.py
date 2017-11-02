#!/usr/bin/python
# init_db.py - create database and initiate tables 

import os
import sys
import MySQLdb
import ConfigParser
import optparse

#use os.path to find the directory of script
bindir = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(bindir+'/config.ini')

# get mysql configurations
host = config.get('database', 'host')
port = config.get('database', 'port')
db   = config.get('database', 'db')
user = config.get('database', 'username')
pwd  = config.get('database', 'password')

# get options from script arguments and store into mysql variables
usage = '''
   - init_db.py - initiation mysql database
   - usage: %prog [options] arg1 arg2...'''
parser = optparse.OptionParser(usage=usage)

option_list = ['host','database','username','password']
for option in option_list:
    parser.add_option('-'+option[0].upper(),
                      "--"+option,
                      action="store",
                      dest=option,help=option
                     )

(options, args) = parser.parse_args()
if options.host is not None:
    host = options.host
if options.database is not None:
    db = options.database
if options.username is not None:
    user = options.username
if options.password is not None:
    pwd = options.password

# connect to the MySQL server
try:
    conn = MySQLdb.connect (host, user, pwd, db)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)

#drop database if exists, and create new database
cursor = conn.cursor ()

print "drop database %s if exists" % db
try: 
    cursor.execute ("DROP DATABASE IF EXISTS %s" % db)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
except:
    print "No existing database %s" % db

print "create database %s" % db
cursor.execute ("CREATE DATABASE %s" % db)
conn.close()

# create database tables from sql file
cmd = "mysql -h%s -P%s -u%s -p%s " % (host, port, user, pwd)
init_sql = bindir + "/table/create.mysql.sql";
print "#init\n mysql %s < %s\n" % (db, init_sql);
os.system("%s %s < %s" % (cmd, db, init_sql));

print "...\nmysql database generated, done."

# ===============  END ============== #
#Usage: 
#   - init_db.py - initiation mysql database
#   - usage: ini_db.py [options] arg1 arg2...
#
#Options:
#  -h, --help            show this help message and exit
#  -H HOST, --host=HOST  host
#  -D DATABASE, --database=DATABASE
#                        database
#  -U USERNAME, --username=USERNAME
#                        username
#  -P PASSWORD, --password=PASSWORD
#                        password
#