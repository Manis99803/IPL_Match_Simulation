#Steps to load files from local machine into hdfs

1. Open terminal and type
	#optional: all the files stored in hdfs will be removed
			   $ hdfs namenode -format
	$ start-dfs.sh
	$ start-yarn.sh
	$ jps  
		Should give something like this	
		(	7680 Jps
			7440 NodeManager
			6625 NameNode
			7274 ResourceManager
			7066 SecondaryNameNode
			6828 DataNode
		)

2. To create a folder on hdfs
	$ hadoop fs -mkdir -p /folder1

3. To load files into hdfs folder created
   Open terminal inside the folder where file is present and type

   $ hadoop fs -put ./file1.csv /folder1

   TO CHECK LOADED FILES

   i) Open browser and type 
   		-localhost:50070
   		-Click on Utilities-> Browse the file system 
   		 (folder that you created should be present)

   ii) Open terminal and type
   		$ hadoop fs -ls /.


#Steps to load hdfs files into pyspark

1. Open terminal and type
	$ pyspark
	(should open jupyter notebook)

2. Open terminal and type
	$ hdfs dfs -chmod -R 777 /folder1
	$ hdfs dfs -chmod -R 777 /folder1/file1.csv

3. Goto the folder where hadoop is installed and open core-site.txt file (path will be something like hadoop/etc/hadoop/core-site.txt)
 --Search fs default name value {eg: hdfs://localhost:9000}

 4. In spark code whereever the path of file1.csv is needed, add
 		hdfs://localhost:portnumber/filepath
 		eg: hdfs://localhost:9000/folder1/file1.csv

#Steps to load files from local machine into pyspark

1. Open terminal and type
	$ pyspark
	(should open jupyter notebook)

2. In spark code whereever the path of file1.csv is needed, add
 	file:///path_to_the_file

 	Eg:file:///home/myname/Desktop/file.csv