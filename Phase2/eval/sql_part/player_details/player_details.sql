drop database bigdata;
create database bigdata;

drop table bowl_vul;
create table bowl_vul
(
	bowler varchar(30),
	batsman varchar(30),
	runs float(10),
	balls float(10),
	prob float(10)
);

drop table bats_vul;
create table bats_vul
(
	batsman varchar(30),
	bowler varchar(30),
	wickets float(10),
	balls float(10),
	prob float(10)
);

drop table profile;
create table profile
(
	player varchar(30),
	bat_avg float(50),
	bowl_avg float(50)
);
