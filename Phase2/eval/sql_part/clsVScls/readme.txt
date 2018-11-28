#File details:

1. clsVScls.sql - will create database with tables mentioned in the code
2. clsVScls.py  - will populate the DB tables by reading values from csv files
	        - performs sql query and creates output csv file clsVScls_otp.csv 

#Steps to run the code:

1. Open terminal and type following commands to create database
	
	#Connects to postgres user
	$ sudo su - postgres
	
	#Change directory
	$ cd /path_to_your_sql_file
	
	#List all sql files
	$ ls -l * sql (this should show .sql file)
	
	#Executing sql file
	$ psql -af clsVScls.sql
	

2. Open terminal inside the folder where clsVScls.py file is present and type
	$ python3 clsVScls.py
	(don't forget to change postgres password and path according to your requirements)
	
Note: 
1. clsVScls_otp.csv will not have all clsVScls details(i.e 10*10 = 100 rows)
 	You need to add remaining pairs and add probability values by giving equal preference to every outcome
	(is already there in clsVScls.csv)

2. Software requirements
	-- postresql
		($ sudo apt-update
		 $ sudo apt-install postgresql postgresql-contrib)
	-- python3
	-- psycopg2 library for python3
		($ pip install psycopg2)
	

