import psycopg2
import csv
import sys

#replace ******* with your postgres password
conn = psycopg2.connect(host="localhost",user = "postgres",password = "*******",database = "postgres") 
cur = conn.cursor()

#PlayerInfo.csv format: batsman_name, bowler_name, P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)
#P(x) - probability of batsman_name getting x against bowler_name
with open('/home/pratheeksha/Desktop/bd/sql_part/clsVScls/inputs/PlayerInfo.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'playerinfo', sep=',')
conn.commit()

#bats_cluster.csv format: batsman_name, bats_cluster_number
with open('/home/pratheeksha/Desktop/bd/sql_part/clsVScls/inputs/bats_cluster.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'batsmancluster', sep=',')
conn.commit()

#bowl_cluster.csv format: bowler_name, bowl_cluster_number
with open('/home/pratheeksha/Desktop/bd/sql_part/clsVScls/inputs/bowl_cluster.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'bowlercluster', sep=',')
conn.commit()

#sql query to generate desired table
sql= "COPY (select batc, bowlc, avg(p_0) as avg_p0, avg(p_1) as avg_p1, avg(p_2) as avg_p2,avg(p_3) as avg_p3, avg(p_4) as avg_p4, avg(p_6) as av_p6, avg(p_w) as avg_pW from (select *, b2.clusternumber as bowlc from ( select *, b1.clusternumber as batc from playerinfo as p1,batsmancluster as b1  where p1.batsman=b1.batsman ) as t1, bowlercluster as b2 where t1.bowler=b2.bowler ) as newtable group by batc, bowlc order by batc, bowlc) TO STDOUT WITH CSV DELIMITER ','"

#clsVscls_otp.csv format: batsman_clusternum, bolwer_clusternum, P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)
#P(x) - probability of batsman belonging to batsman_clusternum getting x against bowler belonging to bowler_clusternum
with open("/home/pratheeksha/Desktop/bd/sql_part/clsVScls/output/clsVscls_otp.csv", "w") as file:
    w = csv.writer(file)
    w.writerow(["Batm_cluster", "Bowl_cluster", "P(0)","P(1)", "P(2)", "P(3)", "P(4)", "P(6)", "P(W)"])
    cur.copy_expert(sql, file)