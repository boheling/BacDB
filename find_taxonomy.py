#!/usr/bin/python
# find_taxonomy.py - retrieve the taxonomy information of given taxID

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

input_file = bindir+'/data/test_tax.txt'

# get options from script arguments and store into mysql variables
usage = '''
   - init_db.py - initiation mysql database
   - usage: %prog [options] arg1 arg2...'''
parser = optparse.OptionParser(usage=usage)

option_list = ['host','database','username','password', 'input_file']
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
if options.input_file is not None:
    input_file = options.input_file
    
# connect to the MySQL server
try:
    conn = MySQLdb.connect (host, user, pwd, db)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)

#drop database if exists, and create new database
cursor = conn.cursor ()

with open(input_file, 'r') as tax_f:
    for line in tax_f:
        taxID = int(line.rstrip('\n'))
        print str(taxID) + '\t',
        while taxID != 1:
            query = """SELECT name_txt, parent_tax_id, rank
                    FROM tax_node, tax_name
                    WHERE tax_node.tax_id = tax_name.tax_id
                    AND name_class = 'scientific name'
                    AND tax_name.tax_id='%s'""" % (taxID)
            cursor.execute(query)
            res=cursor.fetchone()
            if res == None:
                print 'empty',
                break
            tax_name, parent_taxID, rank = res[0:3]
            print rank + '=' + tax_name + '\t',
            taxID = parent_taxID
        print 