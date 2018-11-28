import random
import csv
import math
import os
import time

#format: {batsman_name: {bowler_name:P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)}}
#P(x) - probability of getting x when batsman-bowler pair is played
playerInfoData = {}		

#dictionary which will have the details of all the player of team one of the current match
#format: {batsman_name_team1: {bowler_name_team2:P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)}}	
#P(x) - cumulative probability of getting x when batsman-bowler pair is played								
probabilityDictionaryTeamOne = {}	

#dictionary which will have the details of all the player of team two of the current match
#format: {batsman_name_team2: {bowler_name_team1:P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)}}	
#P(x) - cumulative probability of getting x when batsman-bowler pair is played					
probabilityDictionaryTeamTwo = {}	

#format: {batsman_name: cluster_number}					
batsmanClusterDictionary = {}	

#format: {bowler_name: cluster_number}						
bolwerClusterDictionary = {}	

#format: { clusternumber: {cluster_num:P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)}}						
clusterProbabiltiy = {}	

batsmanClusterCentriods = []
bowlerClusterCentriods = []

batord_team2 = []
batord_team1 = []
bowlord_team2 = []
bowlord_team1 = []

winner = ''

#reading from csvs and storing them in dictionaries
def preProcessing():
	
	#PlayerInfo.csv format: batsman_name, bowler_name, P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)
	filePointer = open("inp_csvs/UpdatedPlayerInfo.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		if i[0] not in playerInfoData:
			playerInfoData[i[0]] = {}
			
		try:
			playerInfoData[i[0]].update({i[1]:{0:float(i[2]), 1:float(i[3]), 2:float(i[4]), 3:float(i[5]), 4:float(i[6]), 6:float(i[7]), "W":float(i[8])}})
		except:
			playerInfoData[i[0]].update({i[1]:{0:float(i[2]), 1:float(i[3]), 2:float(i[4]), 3:float(i[5]), 4:float(i[6]), 6:float(i[7]), "W":0}})
	filePointer.close()

	#BatsmanCluster CSV format : BatsmanName,ClusterNumber
	filePointer = open("inp_csvs/bats_cluster.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		batsmanClusterDictionary[i[0]] = int(i[1])
	filePointer.close()

	#BowlerCluster CSV format : BowlerName,ClusterNumber
	filePointer = open("inp_csvs/bowl_cluster.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		bolwerClusterDictionary[i[0]] = int(i[1])
	filePointer.close()

	#Cluster vs cluster csv format: batsmancls_num, bowlercls_num, P(0), P(1), P(2), P(3), P(4), P(6), P(wicket)
	filePointer = open("inp_csvs/clsVScls.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		if i[0] not in clusterProbabiltiy:
			clusterProbabiltiy[i[0]] = {}
		clusterProbabiltiy[i[0]].update({i[1]:{0:float(i[2]),1:float(i[3]),2:float(i[4]),3:float(i[5]),4:float(i[6]),6:float(i[7]),"W":float(i[8])}})
	filePointer.close()


	#BatsmanClusterCentroids.csv format: cluster_number, centroid
	filePointer = open("inp_csvs/bats_centroids.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		batsmanClusterCentriods.append([float(i[0]),float(i[1])])
	filePointer.close()

	#BowlerClusterCentrois.csv : cluster_number, centroid
	filePointer = open("inp_csvs/bowl_centroids.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		bowlerClusterCentriods.append([ float(i[0]),float(i[1])])
	filePointer.close()

def getBatsmanClusterNumber(name):
	#if we already know the cluster number to which batsman belongs to
	for key,value in batsmanClusterDictionary.items():
		if name == key:
			return value

	#else get batsman's strike_rate and average
	#bats_details.csv format: batsman_name, strike_rate, average
	filePointer = open("inp_csvs/bats_details.csv","r")				
	reader = csv.reader(filePointer)
	next(reader)
	newPlayerDetail = []
	for i in reader:
		if i[0] == name:
			newPlayerDetail.extend([i[1],i[2]])
			break
	filePointer.close()
	
	#if details of batsman are not available, randomly take one strike_rate and average
	if(len(newPlayerDetail)==0):
		rnum = random.randint(0,432)
		filePointer = open("inp_csvs/bats_details.csv","r")				
		reader1 = csv.reader(filePointer)
		next(reader1)
		count = 0
		for i in reader1:
			if(count==rnum):
				newPlayerDetail.extend([float(i[1]),float(i[2])])
				break
			count = count+1
	filePointer.close()

	#decide to which cluster batsman belongs to based on his strike_rate and average using Euclidean distances to each cluster centroids.
	try:	
		n =(float(batsmanClusterCentriods[0][0]) - float(newPlayerDetail[0]) )**2 +  (float(batsmanClusterCentriods[0][1]) - float(newPlayerDetail[1])) **2

		minimumDistance = math.sqrt(n)
		clusterNumber = 0									
		for i in range(1,len(batsmanClusterCentriods)):
			n =(float(batsmanClusterCentriods[i][0]) - float(newPlayerDetail[0]) )**2 +  (float(batsmanClusterCentriods[i][1]) - float(newPlayerDetail[1])) **2

			computeDistance = math.sqrt(n)
			if computeDistance < minimumDistance :
				minimumDistance = computeDistance
				clusterNumber = i
	except:
		#print(name, "not in batsman cluster")
		clusterNumber = random.randint(0,9)

	return clusterNumber 						

def getBowlerClusterNumber(name):
	#if we already know the cluster number to which bowler belongs to
	for key,value in bolwerClusterDictionary.items():
		if name == key:
			return value

	#else get bowler's economy, strike_rate,
	#bowl_details.csv format: batsman_name, economy, strike_rate
	filePointer = open("inp_csvs/bowl_details.csv","r")				
	reader = csv.reader(filePointer)
	next(reader)
	newPlayerDetail = []
	for i in reader:
		if i[0] == name:
			newPlayerDetail.extend([i[2],i[1]])
			break
	filePointer.close()

	#if details of bowler are not available, randomly take one economy, strike_rate
	if(len(newPlayerDetail)==0):
		#print(name, "isnt present")
		rnum = random.randint(0,293)
		filePointer = open("inp_csvs/bowl_details.csv","r")				
		reader1 = csv.reader(filePointer)
		next(reader1)
		count = 0
		for i in reader1:
			if(count==rnum):
				newPlayerDetail.extend([float(i[2]),float(i[1])])
				break
			count = count+1
	filePointer.close()

	#decide to which cluster bowler belongs to based on his economy, strike_rate using Euclidean distances to each cluster centroids.
	try:
		n =(float(bowlerClusterCentriods[0][0]) - float(newPlayerDetail[0]) )**2 +  (float(bowlerClusterCentriods[0][1]) - float(newPlayerDetail[1])) **2

		minimumDistance = math.sqrt(n)
		clusterNumber = 0									
		for i in range(1,len(bowlerClusterCentriods)):
			
			#computeDistance = math.sqrt( ( float(batsmanClusterCentriods[i][0]) - float(newPlayerDetail[0]) )**2 + ( float(batsmanClusterCentriods[i][1]) - float(newPlayerDetail[1]) **2) )
			n =(float(bowlerClusterCentriods[i][0]) - float(newPlayerDetail[0]) )**2 +  (float(bowlerClusterCentriods[i][1]) - float(newPlayerDetail[1])) **2

			computeDistance = math.sqrt(n)
			if computeDistance < minimumDistance :
				minimumDistance = computeDistance
				clusterNumber = i
	except:
		#print(name, "not in bowler cluster")
		clusterNumber = random.randint(0,4)
	return clusterNumber 							

#get cumulative probabilities for every batsman-bowler pair in team1 and team2 from playerInfoData and store it in a dictionary
def getProb(team1, team2, d):
	
	for batsmanName in team1:
		d[batsmanName] = {}
		for bolwerName in team2:
			d[batsmanName].update({bolwerName : {0:0,1:0,2:0,3:0,4:0,6:0,"W":[0,0]}})

			if (batsmanName in playerInfoData) and (bolwerName in playerInfoData[batsmanName]): 
				d[batsmanName][bolwerName][0] = round( float( playerInfoData[batsmanName][bolwerName][0] ),3)
				d[batsmanName][bolwerName][1] = round( float( playerInfoData[batsmanName][bolwerName][1]) + float(d[batsmanName][bolwerName][0]),3)
				d[batsmanName][bolwerName][2] = round( float( playerInfoData[batsmanName][bolwerName][2]) + float(d[batsmanName][bolwerName][1]),3)
				d[batsmanName][bolwerName][3] = round( float( playerInfoData[batsmanName][bolwerName][3]) + float(d[batsmanName][bolwerName][2]),3)
				d[batsmanName][bolwerName][4] = round( float( playerInfoData[batsmanName][bolwerName][4]) + float(d[batsmanName][bolwerName][3]),3)
				d[batsmanName][bolwerName][6] = round( float( playerInfoData[batsmanName][bolwerName][6]) + float(d[batsmanName][bolwerName][4]),3)
				try:
					d[batsmanName][bolwerName]["W"] = [round( float( playerInfoData[batsmanName][bolwerName]["W"]),3) ,round( 1-float(playerInfoData[batsmanName][bolwerName]["W"]),3) ]
				except:
					d[batsmanName][bolwerName]["W"] = [0.5,0.5]
			else:
				batsmanClusterNumber = str(getBatsmanClusterNumber(batsmanName))
				bowlerClusterNumber  = str(getBowlerClusterNumber(bolwerName))


				d[batsmanName][bolwerName][0] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][0]),3)
				d[batsmanName][bolwerName][1] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][1]) + float(d[batsmanName][bolwerName][0]),3)
				d[batsmanName][bolwerName][2] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][2]) + float(d[batsmanName][bolwerName][1]),3)
				d[batsmanName][bolwerName][3] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][3]) + float(d[batsmanName][bolwerName][2]),3)
				d[batsmanName][bolwerName][4] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][4]) + float(d[batsmanName][bolwerName][3]),3)
				d[batsmanName][bolwerName][6] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][6]) + float(d[batsmanName][bolwerName][4]),3)
				try:
					d[batsmanName][bolwerName]["W"] = [round( float( clusterProbabiltiy[batsmanName][bolwerName]["W"]),3) ,round( 1-float(clusterProbabiltiy[batsmanName][bolwerName]["W"]),3) ]
				except:

					d[batsmanName][bolwerName]["W"] = [0.5,0.5]

#function whcich decides the output of ball
def calculate(batsman_name, bowler_name, team_no):
	#creating random number
	randomValue = round(random.uniform(0,1),2)  
	runs = 0
	wicket = 0

	if(team_no == 1):
		d = probabilityDictionaryTeamOne
	else:
		d = probabilityDictionaryTeamTwo

	#if probability of not getting out becomes < 0.05, striker gets out
	if(float(d[batsman_name][bowler_name]["W"][1]) < 0.05):
		runs = 0
		wicket =1
		
	else:
		#check where random value generated lies in the cumulative probablitity distribution and decide the runs scored in the=at ball
		d[batsman_name][bowler_name]["W"][1] *= (1 -float(d[batsman_name][bowler_name]["W"][0]))
		for i in range(7):
			if(i!=5 and randomValue <= float(d[batsman_name][bowler_name][i])):
				runs = i
				wicket = 0
				break
	return (runs, wicket)

def simulate_innings1(team_name, count_match):
	#list containing striker and non-striker names
	players = [batord_team1[0], batord_team1[1]]
	#remove striker and non-striker name from batting order of team1
	del batord_team1[0:2]
	bowlerindex = -1

	#initialising variables
	batsman_name= players[1]
	non_striker = players[0]
	
	total_team1 = 0
	num_balls = 0
	overs = 0.0   
	runs = 0.0
	wicket = 0
	total_wickets = 0
	filename = "simulation"+str(count_match)

	#open csv in write mode
	with open(os.path.join(csvpath, filename)+".csv","w") as inputStream:
		writer = csv.writer(inputStream)
		#format in which simulated csv is created
		writer.writerow(["Innings", "Over","Teamname", "Batsman", "Bowler", "Non-striker", "Runs", "Wicket", "Total"])

		#if all wickets are not fallen
		while(total_wickets < 10):
			#increase ball number
			num_balls = num_balls + 1
			b = num_balls % 6
			i = num_balls // 6

			if(b==0):
				b = 6
				i = i-1
			overs = round((0.1 * b) + i,1)
			
			if(overs == 20.1):
				break

			#next over
			if(((runs%2==1) or (b==1))):
				#change the bowler
				if(b==1):
					bowlerindex = bowlerindex + 1
					bowler_name = bowlord_team2[(bowlerindex )%len(bowlord_team2)]
				#change striker and non-striker
				if(wicket!=1):
					temp = batsman_name
					batsman_name = non_striker
					non_striker = temp 
			    
			#predict runs and wickets for that particular ball
			runs, wicket = calculate(batsman_name, bowler_name, 1)
			
			#update runs and wickets
			total_wickets = total_wickets + wicket
			total_team1 = total_team1 + runs

			#row to be added to the simuation csv
			row = [1,overs,team_name,batsman_name, bowler_name, non_striker, runs, wicket, total_team1]

			#if wicket is fallen, remove batsman name from players list
			#get new batsman from batord list and add him to the players list
			if(wicket==1 and len(batord_team1)>0):
				players.remove(batsman_name)
				players.append(batord_team1[0])
				batsman_name = batord_team1[0]
				del batord_team1[0]
			
			#write row into the csv
			writer.writerow(row)
	inputStream.close()
	
	return total_team1

def simulate_innings2(team_name, total_team1, count_match):
	#list containing striker and non-striker names
	players = [batord_team2[0], batord_team2[1]]

	#remove striker and non-striker name from batting order of team1
	del batord_team2[0:2]

	#initialising variables
	bowlerindex = -1
	batsman_name= players[1]
	non_striker = players[0]

	total_team2 = 0
	num_balls = 0
	overs = 0.0   
	total_wickets = 0
	runs = 0.0
	wicket = 0

	filename = "simulation"+str(count_match)

	#open csv in append mode
	with open(os.path.join(csvpath, filename)+".csv","a") as inputStream:
		writer = csv.writer(inputStream)

		#if all wickets are not fallen
		while(total_wickets < 10):
			#increase ball number
			num_balls = num_balls + 1
			b = num_balls % 6
			i = num_balls // 6

			if(b==0):
				b = 6
				i = i-1
			overs = round((0.1 * b) + i,1)
			
			if(overs == 20.1):
				break

			#next over
			if(((runs%2==1) or (b==1))):
				#change the bowler
				if(b==1):
					bowlerindex = bowlerindex + 1
					bowler_name = bowlord_team1[(bowlerindex)%len(bowlord_team1)]
				#change striker and non-striker
				if(wicket!=1):
					batsman_name, non_striker = non_striker, batsman_name
			    
			#predict runs and wickets for that particular ball	
			runs, wicket = calculate(batsman_name, bowler_name, 2)

			#update runs and wickets			
			total_wickets = total_wickets + wicket
			total_team2 = total_team2 + runs

			#row to be added to the simuation csv
			row = [2, overs, team_name, batsman_name, bowler_name, non_striker, runs, wicket, total_team2]
			
			#if wicket is fallen, remove batsman name from players list
			#get new batsman from batord list and add him to the players list
			if(wicket==1 and len(batord_team2)>0):
				players.remove(batsman_name)
				players.append(batord_team2[0])
				batsman_name = batord_team2[0]
				del batord_team2[0]
			
			#write row into the csv
			writer.writerow(row)

			#end the game if team2 total becomes > team1 total
			if(total_team2 > total_team1):
				return total_team2
	inputStream.close()
	return total_team2
		
def getDetails():
	#reading batting order and bowling order of both the teams from match.csv
	fp = open("inp_csvs/match.csv",'r')
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
		batord_team1.append(i[0])
		batord_team2.append(i[1])
		bowlord_team1.append(i[2])
		bowlord_team2.append(i[3])

if __name__ == "__main__":
	preProcessing()
	#path of the folder(simulated_csvs) where simulated csv get stored
	csvpath = 'simulated_csvs'

	#if folder(simulated_csvs) doesn't exist, create one
	if not os.path.exists(csvpath):
		os.makedirs(csvpath)

	team1_name = "RCB"
	team2_name = "KKR"

	correct_pred = 0
	count_match = 0
	getDetails()
	count_match = count_match + 1

	#get cumulative probabilities for every batsam-bowler pair of both the teams
	getProb(batord_team1, bowlord_team2, probabilityDictionaryTeamOne)
	getProb(batord_team2, bowlord_team1, probabilityDictionaryTeamTwo)

	#simuation for first innings
	team1_total = simulate_innings1(team1_name, count_match)
	#simulation for second innings
	team2_total = simulate_innings2(team2_name, team1_total, count_match)

	predicted = team1_name
	#to print whihb team won
	if(team1_total > team2_total):
		print(team1_name,"won!!")
	elif(team1_total==team2_total):
		predicted = "DRAW"
		print("DRAW")
	else:
		predicted = team2_name
		print(team2_name,"won")

	#to print the final scores of both teams 
	print(team1_name, ":", team1_total)
	print(team2_name, ":", team2_total)

	