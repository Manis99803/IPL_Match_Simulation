drop database bigdata;
create database bigdata;

drop table playerinfo;
create table playerinfo 
(
	batsman varchar(20),
	bowler varchar(20),
	p_0 float(10),
	p_1 float(10),
	p_2 float(10),
	p_3 float(10),
	p_4 float(10),
	p_6 float(10),
	p_w float(10)
);
drop table batsmancluster;
create table batsmancluster 
(
	batsman varchar(20),
	clusternumber int
);
drop table bowlercluster;
create table bowlercluster
(
	
	bowler varchar(20),
	clusternumber int
);
