import psycopg2
import csv
import sys

#replace ******* with your postgres password
conn = psycopg2.connect(host="localhost",user = "postgres",password = "*****",database = "postgres") 
cur = conn.cursor()

#Batsman_vulnerability.csv format: 
#(Batsman_name, Bowler_name, num of wickets batsman has lost for bowler, 
# num of balls batsman has faced against bowler, num_of_wickets/num_of_balls )
with open('/home/prathee/Desktop/bd/sql_part/player_details/inputs/Batsman_vulnerability.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'bats_vul', sep=',')
conn.commit()

#Bowler_vulnerability.csv format:
#(Bowler_name, Batsman_name, no_of_runs given by bowler to batsman,
# no_of_balls_faced by batsman against bowler, num_of_runs/num_of_balls )
with open('/home/prathee/Desktop/bd/sql_part/player_details/inputs/Bowler_vulnerability.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'bowl_vul', sep=',')
conn.commit()

#FinalData.csv format: player_name,  batting average, bowling average
with open('/home/prathee/Desktop/bd/sql_part/player_details/inputs/FinalData.csv', 'r') as f:
    next(f)  
    cur.copy_from(f, 'profile', sep=',')
conn.commit()

#sql query to calculate bowler details
sql1= "COPY (select t3.bowler, strike_rate, economy from (select bowler, (sum(balls)/sum(wickets)) as strike_rate from bats_vul group by bowler having sum(wickets)>0  ) as t1, (select t2.bowler, t2.economy from ( select bowler,(sum(runs)/sum(balls))*6 as economy from bowl_vul group by bowler ) as t2, profile where t2.bowler like profile.player  ) as t3 where t3.bowler like t1.bowler) TO STDOUT WITH CSV DELIMITER ','"

#bowl_details.csv format: bowler_name, strike_rate, economy
with open("/home/prathee/Desktop/bd/sql_part/player_details/outputs/bowl_details.csv", "w") as file:
    w = csv.writer(file)
    w.writerow(["bowler", "strike_rate", "economy"])
    cur.copy_expert(sql1, file)
file.close()  


#sql query to calculate batsman details
sql2= "COPY (select profile.player, t1.strike_rate, profile.bat_avg from (select batsman, (sum(runs)/sum(balls))*100 as strike_rate from bowl_vul group by batsman) as t1, profile where profile.player like t1.batsman) TO STDOUT WITH CSV DELIMITER ','"

#bats_details.csv format:  batsman_name, strike_rate, bat_avg
with open("/home/prathee/Desktop/bd/sql_part/player_details/outputs/bats_details.csv", "w") as file:
    w = csv.writer(file)
    w.writerow(["batsman", "strike_rate", "average"])
    cur.copy_expert(sql2, file)
file.close()    


 
 
