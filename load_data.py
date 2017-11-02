#!/usr/bin/python
# load_data.py - load data from multiple files into database 

import os
import sys
import MySQLdb
import ConfigParser
import optparse
import re
import glob
from time import time

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

if options.host != None:
    host = options.host
if options.database != None:
    db = options.database
if options.username != None:
    user = options.username
if options.password != None:
    pwd = options.password

# connect to the MySQL server
try:
    conn = MySQLdb.connect (host, user, pwd, db)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)
cursor = conn.cursor()


# load summary table #
def load_summary():
    print "loading summary file into mysql database..."
    time0 = time()
    
    with open(bindir+'/data/Summary.txt', 'r') as sum_f: 
        first_line = sum_f.readline()   #skip first line
        
        # format: Accession	GenbankAcc Length Taxid ProjectID TaxName Replicon Create Date Update Date
        for line in sum_f:
            items = line.split('\t')
            cursor.execute ("""
                INSERT INTO summary 
                VALUES
                    (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE Accession=%s""", (items+[items[0]]))
            
        query ="SELECT COUNT(*) from summary"
        cursor.execute(query)             #execute query separately
        res=cursor.fetchone()
        total_rows=res[0]      #total rows
        print "Number of rows inserted: %d. Summary data done." % total_rows
        
    conn.commit()
    time1 = time()
    print "total time for summary table: %s seconds" % (time1 - time0)


# load gff table #
def load_gff():
    print "loading summary file into mysql database..."
    time0 = time()
    file_count = 0
    
    dirs = os.listdir(bindir+'/data/all.gff')   #could use glob from module glob instead
    for dir in dirs[1:]:
        mydir = bindir+'/data/all.gff/' + dir;
        files = os.listdir(mydir)
        for file in files:
            if 'gff' in file:
                file_count += 1
                print "inserting gff from file number", file_count
    
                with open(mydir+'/' + file, 'r') as gff_f:
                    skiplines = [gff_f.readline() for _ in xrange(5)]   #skip five lines
                    summary_line = gff_f.readline()     #the species summary line
                    accession = summary_line.split('\t')[0]
                    search_acc_query = "SELECT summaryID FROM summary WHERE Accession='%s'" % (accession)
                    cursor.execute(search_acc_query)
                    res=cursor.fetchone()   #2493L, for example
                    if not res:
                        print "no summary data for %s" % accession
                        break
                    summaryID = int(res[0])
                    
                    #read useful lines
                    while True:
                        try:
                            line = gff_f.readline()
                            if(line == '###\n'):
                                conn.commit()
                                break
                            items = line.split('\t');
                            if(items[2] != 'CDS'):
                                continue
                            new_items = [None if item == '.' else item for item in items] # replace . with empty
                            insertion = [summaryID] + new_items[1:8]     #the items to be inserted into mysql
                            
                            #using re to fetch more information from the line
                            desc_name_list = ['ID', 'Name', 'Dbxref', 'Parent', 'product', 'Note']
                            
                            # change to string API after further splitting
                            m_desc = {}
                            desc_list = items[8].split(';')
                            for desc in desc_list:
                                desc_head, desc_content = desc.split('=')
                                m_desc[desc_head] = desc_content
                                
                            for desc_name in desc_name_list:
                                insertion.append(m_desc[desc_head])
                            
                            # insert into mysql
                            cursor.execute ("""
                                            INSERT INTO gff
                                            VALUES
                                            (NULL, %s, %s, %s, %s, %s, %s,
                                            %s, %s, %s, %s, %s, %s, %s, %s)
                                            """, (insertion))
                        except StopIteration:
                            break # stops the moment you finish reading the file
                        if not line:
                            break # stops the moment you get to an empty line
    
    conn.commit()
    time1 = time()
    print "total time for gff table: %s seconds" % (time1 - time0)


#load tax_files
def load_tax():
    print "loading taxonomy files into mysql database..."
    time0 = time()
    
    print "loading nodes file now"
    count = 0
    with open(bindir+'/data/taxdump/nodes.dmp', 'r') as tnode_f:      
        for line in tnode_f:
            rs_line = line.rstrip('\n')
            items = rs_line.split('|')

            rs_items = [item.replace('\t','') for item in items]
            rs_items.pop()
            cursor.execute ("""
                INSERT INTO tax_node 
                VALUES
                    (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (rs_items))
            count += 1
            if count % 100000 == 0:
                print str(count) + ' inserted'
    print "nodes done."
    
    print "loading tax names now"
    count = 0
    with open(bindir+'/data/taxdump/names.dmp', 'r') as tname_f:      
        for line in tname_f:
            rs_line = line.rstrip('\n')
            items = rs_line.split('|')

            rs_items = [item.replace('\t','') for item in items]
            rs_items.pop()
            cursor.execute ("""
                INSERT INTO tax_name 
                VALUES
                    (NULL, %s, %s, %s, %s)
                """, (rs_items))
            count += 1
            if count % 1000 == 0:
                print str(count) + ' inserted'
        print "names done."
    
    print "loading tax Divisions now"
    count = 0
    with open(bindir+'/data/taxdump/division.dmp', 'r') as tdiv_f:      
        for line in tdiv_f:
            rs_line = line.rstrip('\n')
            items = rs_line.split('|')

            rs_items = [item.replace('\t','') for item in items]
            rs_items.pop()
            cursor.execute ("""
                INSERT INTO tax_div 
                VALUES
                    (NULL, %s, %s, %s, %s)
                """, (rs_items))
            count += 1
            if count % 1 == 0:
                print str(count) + ' inserted'            
    conn.commit()
    time1 = time()
    print "total time for taxonomy tables: %s seconds" % (time1 - time0)

# ===================== #
# main
# ===================== #
load_tax()
files = glob.glob('./*.gff')
conn.close()
