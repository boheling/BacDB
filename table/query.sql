select * from gff;
select * from summary;
SELECT * FROM gff WHERE Product REGEXP 'clpx' group by summaryID;
SELECT * FROM gff WHERE Product REGEXP 'clpx';
SELECT summary.TaxName, gff.* FROM gff,summary WHERE Product REGEXP 'DnaA'and gff.summaryID = summary.summaryID;
SELECT summary.TaxName, gff.* FROM gff,summary WHERE Product REGEXP 'ClpP'and gff.summaryID = summary.summaryID;
SELECT distinct summary.*
FROM summary 
WHERE summary.Replicon REGEXP 'chromosome'
AND summary.summaryID NOT IN (SELECT distinct summary.summaryID FROM summary,gff WHERE gff.Product REGEXP 'clpx' and gff.summaryID=summary.summaryID);
SELECT distinct summary.* FROM summary,gff WHERE gff.Product REGEXP 'clpx' and gff.summaryID=summary.summaryID;