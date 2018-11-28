import random
import csv
import math
import os

playerInfoData = {}											# player Info Dictionary , player vs player data
probabilityDictionaryTeamOne = {}							# dictionary which will have the details of all the player and pair wise probabily of team one of the current match
probabilityDictionaryTeamTwo = {}							# dictionary which will have the details of all the player and pair wise probabily of team two of the current match
batsmanClusterDictionary = {}								# Dicionary with batsman name as key and the value as the cluster number
bolwerClusterDictionary = {}								# Dicionary with bowler name as key and the value as the cluster number
clusterProbabiltiy = {}										# Getting the cluster probabilties
batsmanClusterCentriods = []								# Dictionary which will store all the batsman cluster centroids
bowlerClusterCentriods = []									# Dictionary which will store all the bowler cluster centroids
batord_team1 = []
batord_team2 = []
bowlord_team1 = []
bowlord_team2 = []
team1 = []
team2 = []
winner = ''


def preProcessing():
	
	#PlayerInfo.csv 
	# Loading all the player vs player prob statistics into the playerInfoData dictionary.
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/UpdatedPlayerInfo.csv","r")
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
	# Loading the batsmanu cluster information into the batsmanClsuterDictionary
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bats_res.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		batsmanClusterDictionary[i[0]] = int(i[1])
	filePointer.close()

	#BowlerCluster CSV format : BowlerName,ClusterNumber
	# Loading the bowler cluster information into the bowlerClusterDicitionary
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bowl_res.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		bolwerClusterDictionary[i[0]] = int(i[1])
	filePointer.close()

	#ClusterCSV
	# Loading the cluster probability into the cluster dicitionary
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/clsVScls.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		if i[0] not in clusterProbabiltiy:
			clusterProbabiltiy[i[0]] = {}
		clusterProbabiltiy[i[0]].update({i[1]:{0:float(i[2]),1:float(i[3]),2:float(i[4]),3:float(i[5]),4:float(i[6]),6:float(i[7]),"W":float(i[8])}})
	filePointer.close()


	#BatsmanClusterCentroids.csv
	# Loading the batsman cluster centroids into the batsman cluster centroids dictionary.
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bats_centroids.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		batsmanClusterCentriods.append([float(i[0]),float(i[1])])
	filePointer.close()

	#BowlerClusterCentrois.csv
	# Loading the bowler cluster centroids into the bowler cluster centroids dictionary
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bowl_centroids.csv","r")
	reader = csv.reader(filePointer)
	next(reader)
	for i in reader:
		bowlerClusterCentriods.append([ float(i[0]),float(i[1])])
	filePointer.close()

def getBatsmanClusterNumber(name):
	
	# If player name exist in the database return the cluster to which he belongs.
	for key,value in batsmanClusterDictionary.items():
		if name == key:
			return value

	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bats_details.csv","r")				
	reader = csv.reader(filePointer)
	next(reader)
	newPlayerDetail = []
	for i in reader:
		if i[0] == name:
			newPlayerDetail.extend([i[2],i[1]])
			break
	filePointer.close()
	
	#todo
	if(len(newPlayerDetail)==0):
		rnum = random.randint(0,71)
		filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bats_details.csv","r")				
		reader1 = csv.reader(filePointer)
		next(reader1)
		count = 0
		for i in reader1:
			if(count==rnum):
				newPlayerDetail.extend([float(i[2]),float(i[1])])
				break
			count = count+1
	filePointer.close()
	
	# if the player is not present in the cluster take his statistics and get the minimum euclidean distance by taking his statistics and the cluster centroids ,minimum distance's cluster number is assigned to that player
	try:
		minimumDistance = math.sqrt( ( float(batsmanClusterCentriods[0][0]) - float(newPlayerDetail[0]) )**2 + ( float(batsmanClusterCentriods[0][1]) - float(newPlayerDetail[1]) **2) )			
		clusterNumber = 0									
		for i in range(1,len(batsmanClusterCentriods)):
			computeDistance = math.sqrt( ( float(batsmanClusterCentriods[i][0]) - float(newPlayerDetail[0]) )**2 + ( float(batsmanClusterCentriods[i][1]) - float(newPlayerDetail[1]) **2) )
			if computeDistance < minimumDistance :
				minimumDistance = computeDistance
				clusterNumber = i
	except:
		clusterNumber = random.randint(0,3)
	return clusterNumber 						

def getBowlerClusterNumber(name):


	# If player name exist in the database return the cluster to which he belongs.
	for key,value in bolwerClusterDictionary.items():
		if name == key:
			return value
	
	#Details.csv has the average and strike rate if any new player is playing the match. Format : Name, Economy ,Strike Rate
	filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bowl_details.csv","r")				
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
		rnum = random.randint(0,293)
		filePointer = open("/home/manish/Downloads/final_phase2eval/eval/inp_csvs/bowl_details.csv","r")				
		reader1 = csv.reader(filePointer)
		next(reader1)
		count = 0
		for i in reader1:
			if(count==rnum):
				newPlayerDetail.extend([float(i[2]),float(i[1])])
				break
			count = count+1
	filePointer.close()

	# if the player is not present in the cluster take his statistics and get the minimum euclidean distance by taking his statistics and the cluster centroids ,minimum distance's cluster number is assigned to that player
	try:
		minimumDistance = math.sqrt(( (bowlerClusterCentriods[0][0] - newPlayerDetail[0])**2) + ((bowlerClusterCentriods[0][1] - newPlayerDetail[1])**2) ) 		
		clusterNumber = 0									
		for i in range(1,len(bowlerClusterCentriods)):
			computeDistance = math.sqrt(( (bowlerClusterCentriods[i][0] - newPlayerDetail[0])**2) + ((bowlerClusterCentriods[i][1] - newPlayerDetail[1])**2) )		#Computing the euclidean distance
			if computeDistance < minimumDistance:
				minimumDistance = computeDistance
				clusterNumber = i
	except:
		clusterNumber = random.randint(0,3)
	return clusterNumber 							

def getProb(team1, team2, d):
	
	for batsmanName in team1:
		d[batsmanName] = {}
		for bolwerName in team2:
			# ditionary format batsman : { bowler : 0 : prob(0), 1: prob(1), 2: prob(2), 3: prob(3), 4: prob(4), 6: prob(6), "W":[prob(W),1-prob(W)]}
			d[batsmanName].update({bolwerName : {0:0,1:0,2:0,3:0,4:0,6:0,"W":[0,0]}})

			# If the batsman and bowler pair exist in the player vs player info get the corresponding probabilities and compute the cumulative probability.
			if (batsmanName in playerInfoData) and (bolwerName in playerInfoData[batsmanName]): 
				d[batsmanName][bolwerName][0] = round( float( playerInfoData[batsmanName][bolwerName][0] ),3)
				d[batsmanName][bolwerName][1] = round( float( playerInfoData[batsmanName][bolwerName][1]) + float(playerInfoData[batsmanName][bolwerName][0]),3)
				d[batsmanName][bolwerName][2] = round( float( playerInfoData[batsmanName][bolwerName][2]) + float(playerInfoData[batsmanName][bolwerName][1]),3)
				d[batsmanName][bolwerName][3] = round( float( playerInfoData[batsmanName][bolwerName][3]) + float(playerInfoData[batsmanName][bolwerName][2]),3)
				d[batsmanName][bolwerName][4] = round( float( playerInfoData[batsmanName][bolwerName][4]) + float(playerInfoData[batsmanName][bolwerName][3]),3)
				d[batsmanName][bolwerName][6] = round( float( playerInfoData[batsmanName][bolwerName][6]) + float(playerInfoData[batsmanName][bolwerName][4]),3)
				try:
					d[batsmanName][bolwerName]["W"] = [round( float( playerInfoData[batsmanName][bolwerName]["W"]),3) ,round( 1-float(playerInfoData[batsmanName][bolwerName]["W"]),3) ]
				except:
					d[batsmanName][bolwerName]["W"] = [0.5,0.5]
			else:

				# If the batsman and bowler doesn't exist in the player vs player info ,get the cluster number to which the batsman and bowler belongs.
				batsmanClusterNumber = str(getBatsmanClusterNumber(batsmanName))
				bowlerClusterNumber  = str(getBowlerClusterNumber(bolwerName))

				# Take the cluster number and set the cluster probabilty as the probabilty for the batsman bowler pair,and compute the cumulative probabilty.
				d[batsmanName][bolwerName][0] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][0]),3)
				d[batsmanName][bolwerName][1] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][1]) + float(clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][0]),3)
				d[batsmanName][bolwerName][2] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][2]) + float(clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][1]),3)
				d[batsmanName][bolwerName][3] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][3]) + float(clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][2]),3)
				d[batsmanName][bolwerName][4] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][4]) + float(clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][3]),3)
				d[batsmanName][bolwerName][6] = round( float( clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][6]) + float(clusterProbabiltiy[batsmanClusterNumber][bowlerClusterNumber][4]),3)
				try:
					d[batsmanName][bolwerName]["W"] = [round( float( clusterProbabiltiy[batsmanName][bolwerName]["W"]),3) ,round( 1-float(clusterProbabiltiy[batsmanName][bolwerName]["W"]),3) ]
				except:
					d[batsmanName][bolwerName]["W"] = [0.5,0.5]



def getTeamDetails(path):
	global winner
	with open(path,"r") as inputStream:
	
		reader = csv.reader(inputStream)
		next(reader)
		row  = [r for r in reader]
		
		team1_name = row[0][2]
		team2_name = row[1][2]
		toss_winner = row[8][2]
		toss_decision = row[9][2]
		winner = row[17][2]

		if(team1_name != toss_winner):
			team1_name, team2_name = team2_name, team1_name
		print(team1_name, "won the toss")

		if(toss_decision != 'bat'):
			team1_name, team2_name = team2_name, team1_name
		print(team1_name,"chose to bat\n")

		print("************************************************************")
		print("*********",team1_name, "VS", team2_name,"*********")
		print("************************************************************\n")
		
		row = row[18:-1]
		innings1 = []
		innings2 = []

		# Iterate over the input csv
		for i in range(len(row)):
			
			if(row[i][1]=='1'):
				if(row[i][4] not in team1):
					team1.append(row[i][4])
				if(row[i][4] not in batord_team1):
					batord_team1.append(row[i][4])     			 # Buidling the batting order of the team1

				if(row[i][6] not in team2):
					team2.append(row[i][6])
				if(row[i][6] not in bowlord_team2):
					bowlord_team2.append(row[i][6])				# Building the bowling order of the team2


			elif(row[i][1]=='2'):
				if(row[i][4] not in team2):
					team2.append(row[i][4])
				if(row[i][4] not in batord_team2):
					batord_team2.append(row[i][4])				# Building the bowling order of the team2

				if(row[i][6] not in team1):
					team1.append(row[i][6])
				if(row[i][6] not in bowlord_team1):
					bowlord_team1.append(row[i][6])				# Building the bowling order of the team1

	inputStream.close()
	# Getting the probabilty after getting the team, bowling order
	getProb(team1, bowlord_team2, probabilityDictionaryTeamOne)
	getProb(team2, bowlord_team1, probabilityDictionaryTeamTwo)

	return (team1_name, team2_name)
		

def calculate(batsman_name, bowler_name, team_no):


	# get the random value for the score prediction and rounding it of two decimal places
	randomValue = round(random.uniform(0,1),2)  
	runs = 0
	wicket = 0

	if(team_no == 1):
		d = probabilityDictionaryTeamOne
	else:
		d = probabilityDictionaryTeamTwo

	# If the probabilty goes below some this threshold he is declared out
	if(float(d[batsman_name][bowler_name]["W"][1]) < 0.05):
		runs = 0
		wicket =1
		
	else:
		
		# update the prob of 1 - prob(W) 
		d[batsman_name][bowler_name]["W"][1] *= (1 -float(d[batsman_name][bowler_name]["W"][0]))
		for i in range(7):
			if(i!=5 and randomValue <= float(d[batsman_name][bowler_name][i])):
				runs = i
				wicket = 0
				break
	
	
	return (runs, wicket)

def simulate_innings1(team_name, count_match):
	
	players = [team1[0], team1[1]]
	del team1[0:2]							# delete the firsttwo batsman from the list
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
	
	# Storing the simulation in a file
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
			# If an odd run is scored or if the over is completed strike is changed,and bowler is changed by taking the bowler at next index from the bowler list
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

	# Appending to the same file which was created when simulating the first inning.
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
			# If an odd run is scored or if the over is completed strike is changed,and bowler is changed by taking the bowler at next index from the bowler list
			if(((runs%2==1) or (b==1))):
				if(b==1):
					bowlerindex = bowlerindex + 1
					bowler_name = bowlord_team1[(bowlerindex)%len(bowlord_team1)]
				
				# If wicket has not fallen then we swap the players 	
				if(wicket!=1):
					batsman_name, non_striker = non_striker, batsman_name
			    
			
			# calling calucate function which gets the run and wicket by taking the batsman and bowler
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

if __name__ == "__main__":

	# Function which does the job of all loading data player vs player, cluster vs cluster data into the dictionary etc .,
	preProcessing()
	
	#path of the folder to be created
	csvpath = '/home/manish/Downloads/final_phase2eval/eval/simulated_matches'
	path = "/home/manish/Downloads/final_phase2eval/eval/test_matches"
	supported_formats = ('.csv')

	# Get paht of the all the files which are to be simulated
	path_list = [os.path.join(path, fname) for fname in os.listdir(path) if fname.lower().endswith(supported_formats)]

	csvpath = '/home/manish/Downloads/final_phase2eval/eval/simulated_csvs'
	if not os.path.exists(csvpath):
		os.makedirs(csvpath)

	correct_pred = 0
	count_match = 0

	# Iterate over all the matches.
	for filename in path_list:
		count_match = count_match + 1
		team1_name, team2_name =  getTeamDetails(filename)

		team1_total = simulate_innings1(team1_name, count_match)
		team2_total = simulate_innings2(team2_name, team1_total, count_match)

		print(team1_total)
		print(team2_total)
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
			print("Good prediction")
			correct_pred = correct_pred + 1

	accuracy = correct_pred / count_match
	print("Accuracy :", accuracy)
