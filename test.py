# ===================== #
# load summary table
# ===================== #
print "loading summary file into mysql database..."
time0 = time()
with open(bindir+'/data/taxdump/nodes.dmp', 'r') as sum_f: 
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