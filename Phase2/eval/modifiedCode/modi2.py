import random
import csv
import math
import os

playerInfoData = {}											#player Info Dictionary
probabilityDictionaryTeamOne = {}							#dictionary which will have the details of all the player of team one of the current match
probabilityDictionaryTeamTwo = {}							#dictionary which will have the details of all the player of team two of the current match
batsmanClusterDictionary = {}								#Dicionary with batsman name as key and the value as the cluster number
bolwerClusterDictionary = {}								#Dicionary with bowler name as key and the value as the cluster number
clusterProbabiltiy = {}										#Getting the cluster probabilties
batsmanClusterCentriods = []
bowlerClusterCentriods = []

team2 = ["BB McCullum","Q de","V Kohli","AB de","SN Khan","Mandeep Singh","CR Woakes","Wahsington Sundar","UT Yadav","Kulwant Khejroliya","YS Chahal"]
team1 = ["SP Narine","CA Lynn","RV Uthappa","N Rana","Dinesh Karthik","Rinku Singh","AD Russell","R Vinay","PP Chawla","MG Johnson","Kuldeep Yadav"]

batord_team2 =  ["BB McCullum","Q de","V Kohli","AB de","SN Khan","Mandeep Singh","CR Woakes","Wahsington Sundar","UT Yadav","Kulwant Khejroliya","YS Chahal"]
batord_team1 =  ["SP Narine","CA Lynn","RV Uthappa","N Rana","Dinesh Karthik","Rinku Singh","AD Russell","R Vinay","PP Chawla","MG Johnson","Kuldeep Yadav"]

bowlord_team2 = ["Y Chahal","CA Woakes","Wahsington Sundar","UT Yadav","Kulwant Khejroliya"]
bowlord_team1 = ["R Vinay","PP Chawla","Kuldeep Yadav","SP Narine","MG Johnson","AD Russell","N Rana"]

winner = ''
def preProcessing():
	
	#PlayerInfo.csv
	filePointer = open("UpdatedPlayerInfo.csv","r")
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
	filePointer = open("bats_cluster.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		batsmanClusterDictionary[i[0]] = int(i[1])
	filePointer.close()

	#BowlerCluster CSV format : BowlerName,ClusterNumber
	filePointer = open("bowl_cluster.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		bolwerClusterDictionary[i[0]] = int(i[1])
	filePointer.close()

	#ClusterCSV
	filePointer = open("clsvscls.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		if i[0] not in clusterProbabiltiy:
			clusterProbabiltiy[i[0]] = {}
		clusterProbabiltiy[i[0]].update({i[1]:{0:float(i[2]),1:float(i[3]),2:float(i[4]),3:float(i[5]),4:float(i[6]),6:float(i[7]),"W":float(i[8])}})
	filePointer.close()


	#BatsmanClusterCentroids.csv
	filePointer = open("bats_centroids.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		batsmanClusterCentriods.append([float(i[0]),float(i[1])])
	filePointer.close()

	#BowlerClusterCentrois.csv
	filePointer = open("bowl_centroids.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		bowlerClusterCentriods.append([ float(i[0]),float(i[1])])
	filePointer.close()

def getBatsmanClusterNumber(name):
	for key,value in batsmanClusterDictionary.items():
		if name == key:
			return value


	filePointer = open("bats_details.csv","r")				
	reader = csv.reader(filePointer)
	next(reader)
	newPlayerDetail = []
	for i in reader:
		if i[0] == name:
			newPlayerDetail.extend([i[1],i[2]])
			break
	filePointer.close()
	#print(name)
	#todo
	if(len(newPlayerDetail)==0):
		rnum = random.randint(0,432)
		filePointer = open("bats_details.csv","r")				
		reader1 = csv.reader(filePointer)
		next(reader1)
		count = 0
		for i in reader1:
			if(count==rnum):
				newPlayerDetail.extend([float(i[1]),float(i[2])])
				break
			count = count+1
	filePointer.close()
	#print(newPlayerDetail)
	#print(batsmanClusterCentriods)
	try:
		
		n =(float(batsmanClusterCentriods[0][0]) - float(newPlayerDetail[0]) )**2 +  (float(batsmanClusterCentriods[0][1]) - float(newPlayerDetail[1])) **2

		minimumDistance = math.sqrt(n)
		clusterNumber = 0									
		for i in range(1,len(batsmanClusterCentriods)):
			
			#computeDistance = math.sqrt( ( float(batsmanClusterCentriods[i][0]) - float(newPlayerDetail[0]) )**2 + ( float(batsmanClusterCentriods[i][1]) - float(newPlayerDetail[1]) **2) )
			n =(float(batsmanClusterCentriods[i][0]) - float(newPlayerDetail[0]) )**2 +  (float(batsmanClusterCentriods[i][1]) - float(newPlayerDetail[1])) **2

			computeDistance = math.sqrt(n)
			if computeDistance < minimumDistance :
				minimumDistance = computeDistance
				clusterNumber = i
	except:
		print(name, "not in batsman cluster")
		clusterNumber = random.randint(0,10)


	return clusterNumber 						

def getBowlerClusterNumber(name):
	for key,value in bolwerClusterDictionary.items():
		if name == key:
			return value
	#Details.csv has the average and strike rate if any new player is playing the match. Format : Name, Economy ,Strike Rate
	filePointer = open("bowl_details.csv","r")				
	reader = csv.reader(filePointer)
	next(reader)
	newPlayerDetail = []
	for i in reader:
		if i[0] == name:
			newPlayerDetail.extend([i[2],i[1]])
			break
	filePointer.close()

	#no matching data for that player
	if(len(newPlayerDetail)==0):
		#print(name, "isnt present")
		rnum = random.randint(0,293)
		filePointer = open("bowl_details.csv","r")				
		reader1 = csv.reader(filePointer)
		next(reader1)
		count = 0
		for i in reader1:
			if(count==rnum):
				newPlayerDetail.extend([float(i[2]),float(i[1])])
				break
			count = count+1
	filePointer.close()

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
		print(name, "not in bowler cluster")
		clusterNumber = random.randint(0,4)
	return clusterNumber 							

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


	

def calculate(batsman_name, bowler_name, team_no):
	randomValue = round(random.uniform(0,1),2)  
	print(randomValue)
	runs = 0
	wicket = 0

	if(team_no == 1):
		d = probabilityDictionaryTeamOne
	else:
		d = probabilityDictionaryTeamTwo

	#print(float(d[batsman_name][bowler_name]["W"][0]))
	if(float(d[batsman_name][bowler_name]["W"][1]) < 0.05):
		runs = 0
		wicket =1
		
	else:
		d[batsman_name][bowler_name]["W"][1] *= (1 -float(d[batsman_name][bowler_name]["W"][0]))
		#print("total prob = ", float(d[batsman_name][bowler_name][6]))
		for i in range(7):
			if(i!=5 and randomValue <= float(d[batsman_name][bowler_name][i])):
				print("prob = ",float(d[batsman_name][bowler_name][i]), "runs = ",i)
				runs = i
				wicket = 0
				break
	return (runs, wicket)

def simulate_innings1(team_name, count_match):
	
	players = [team1[0], team1[1]]
	del team1[0:2]
	bowlerindex = -1

	batsman_name= players[1]
	non_striker = players[0]
	
	total_team1 = 0
	num_balls = 0
	overs = 0.0   
	runs = 0.0
	wicket = 0
	total_wickets = 0
	filename = "simulation"+str(count_match)
	
	with open(os.path.join(csvpath, filename)+".csv","w") as inputStream:
		writer = csv.writer(inputStream)
		writer.writerow(["Innings", "Over","Teamname", "Batsman", "Bowler", "Non-striker", "Runs", "Wicket", "Total"])

		while(total_wickets < 10):
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
				if(b==1):
					bowlerindex = bowlerindex + 1
					bowler_name = bowlord_team2[(bowlerindex )%len(bowlord_team2)]
				if(wicket!=1):
					temp = batsman_name
					batsman_name = non_striker
					non_striker = temp 
			    
			
			runs, wicket = calculate(batsman_name, bowler_name, 1)
			total_wickets = total_wickets + wicket

			total_team1 = total_team1 + runs
			row = [1,overs,team_name,batsman_name, bowler_name, non_striker, runs, wicket, total_team1]

			if(wicket==1 and len(team1)>0):
				players.remove(batsman_name)
				players.append(team1[0])
				batsman_name = team1[0]
				del team1[0]
			
			
			writer.writerow(row)
	inputStream.close()
	
	return total_team1

def simulate_innings2(team_name, total_team1, count_match):

	print(len(bowlord_team1))
	players = [team2[0], team2[1]]
	del team2[0:2]
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

	with open(os.path.join(csvpath, filename)+".csv","a") as inputStream:
		writer = csv.writer(inputStream)

		while(total_wickets < 10):
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
				if(b==1):
					bowlerindex = bowlerindex + 1
					bowler_name = bowlord_team1[(bowlerindex)%len(bowlord_team1)]
					
				if(wicket!=1):
					batsman_name, non_striker = non_striker, batsman_name
			    
			
			runs, wicket = calculate(batsman_name, bowler_name, 2)
			total_wickets = total_wickets + wicket

			total_team2 = total_team2 + runs
			row = [2, overs, team_name, batsman_name, bowler_name, non_striker, runs, wicket, total_team2]
			if(wicket==1 and len(batord_team2)>0):
				players.remove(batsman_name)
				players.append(team2[0])
				batsman_name = team2[0]
				del batord_team2[0]
			
			writer.writerow(row)

			if(total_team2 > total_team1):
				return total_team2
	inputStream.close()
	return total_team2

def getTeamDetails(path):
	global winner
	with open(path,"r") as inputStream:
	
		reader = csv.reader(inputStream)
		next(reader)
		row  = [r for r in reader]
		
		team1_name = "MI"
		team2_name = "DD"
		toss_winner = "MI"


		print("************************************************************")
		print("*********",team1_name, "VS", team2_name,"*********")
		print("************************************************************\n")

		innings1 = []
		innings2 = []

		
		for i in range(len(row)):
			team1.append(row[i][0])
			team2.append(row[i][1])

			batord_team1.append(row[i][0])
			bowlord_team1.append(row[i][0])

			batord_team2.append(row[i][1])
			bowlord_team2.append(row[i][1])

	inputStream.close()
	getProb(team1, bowlord_team2, probabilityDictionaryTeamOne)
	getProb(team2, bowlord_team1, probabilityDictionaryTeamTwo)

	return (team1_name, team2_name)
		

if __name__ == "__main__":
	preProcessing()
	#path of the folder to be created
	csvpath = '/home/manish/Downloads/final_phase2eval/eval/modifiedCode/simulated_csvs'

	if not os.path.exists(csvpath):
		os.makedirs(csvpath)

	team1_name = "MI"
	team2_name = "DD"

	correct_pred = 0
	count_match = 0

	count_match = count_match + 1
	getProb(team1, bowlord_team2, probabilityDictionaryTeamOne)
	getProb(team2, bowlord_team1, probabilityDictionaryTeamTwo)
	team1_total = simulate_innings1(team1_name, count_match)
	team2_total = simulate_innings2(team2_name, team1_total, count_match)


	predicted = team1_name
	if(team1_total > team2_total):
		print(team1_name,"won!!")
	elif(team1_total==team2_total):
		predicted = "DRAW"
		print("DRAW")
	else:
		predicted = team2_name
		print(team2_name,"won")


	if(predicted==winner):
		print("Correct prediction\n")
		correct_pred = correct_pred + 1
	else:
		print("Wrong prediction\n")
	

	print(team1_name, ":", team1_total)
	print(team2_name, ":", team2_total)
	#Baccuracy = correct_pred / count_match
	#rint("Accuracy :", accuracy)
	