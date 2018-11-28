#File details:

1. player_details.sql - will create database with tables mentioned in the code
2. player_details.py  - will populate the DB tables by reading values from csv files
		 - performs sql query and creates output csvs bats_details.csv and bowl_details.csv

#steps to run the code:

1. Open terminal and type following commands to create database
	
	#Connects to postgres user
	$ sudo su - postgres
	
	#Change directory
	$ cd /path_to_your_sql_file
	
	#List all sql files
	$ ls -l * sql (this should show .sql file)
	
	#Executing sql file
	$ psql -af player_details.sql
	

2. Open terminal inside the folder where clsVScls.py file is present and type
	$ python3 player_details.py
	(don't forget to change postgres password and path according to your requirements)
	
Note: 
1. Software requirements
	-- postresql
		($ sudo apt-update
		 $ sudo apt-install postgresql postgresql-contrib)
	-- python3
	-- psycopg2 library for python3
		($ pip install psycopg2)
	

