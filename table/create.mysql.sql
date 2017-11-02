create table summary(
    summaryID       integer not null auto_increment,
    Accession       char(40),
    GenbankAcc      char(40),
    Length          int,
    Taxid           integer,
    ProjectID       integer,
    TaxName         text,
    Replicon        char(40),
    Create_Date     char(40),
    Update_Date     char(40),
    PRIMARY KEY (summaryID),
    index(Accession)
);

create table gff(
    gffID       		integer not null auto_increment,
    summaryID       integer,
    source      		char(40),
    type          	char(40),
    start           integer,
    end       			integer,
    score         	float,
    strand        	char(12),
    phase     			char(40),
    att_id    			char(40),
    att_name				char(200),
    Dbxref					text,
    Parent					char(40),
    Product					text,
    Note						text,
    PRIMARY KEY (gffID),
    index(att_name)
);

create table tax_node(
		tax_nodeID											 integer not null auto_increment,
	  tax_id				                   integer,
 	  parent_tax_id	                   integer,
 	  rank					                   char(40),
 	  embl_code			                   char(20),
 	  division_id		                   integer,
 	  inherited_div_flag  	           integer,
 	  genetic_code_id			             integer,
 	  inherited_GC_flag  	           	 integer,
 	  mitochondrial_genetic_code_id	   integer,
 	  inherited_MGC_flag  	           integer,
 	  GenBank_hidden_flag              integer,
 	  hidden_subtree_root_flag         integer,
 	  comments				                 text,
    PRIMARY KEY (tax_nodeID),
    index(tax_id)
);

create table tax_name(
		tax_nameID											 integer not null auto_increment,
		tax_id													 integer, 
		name_txt				                 text,    
		unique_name			                 text,    
		name_class			                 char(40),
    PRIMARY KEY (tax_nameID),
    index(tax_id)
);


create table tax_div(
    tax_divID                        integer not null auto_increment,      
	  division_id				               integer,                              
	  division_cde			               char(20),                                 
	  division_name			               char(40),                                 
	  comments                         text,                             
    PRIMARY KEY (tax_divID)
);