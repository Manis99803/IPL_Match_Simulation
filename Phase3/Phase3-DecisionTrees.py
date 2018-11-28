
# coding: utf-8

# In[ ]:


#loading the data from local machine
from pyspark.sql import SparkSession

#creating a spark session
sparkSession = SparkSession.builder.appName("decision-tree-example").getOrCreate()

#if dataset has header
data = sparkSession.read.csv("file:///home/pratheeksha/Desktop/Phase3/InputCSVS/FinalDataSet.csv", sep=',', header=True)

#if dataset doesn't have header
#data = sparkSession.read.csv("file:///home/pratheeksha/Desktop/Phase3/InputCSVS/FinalDataSet4.csv", sep=',', header=False)

#to see the loaded data
data.show()
print(type(data))


# In[ ]:


#to see the schema of dataframe
data.printSchema()


# In[ ]:


from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

#to create labeledPoint rdd
#which has label(target variable column) and features(all the columns except target variable column)
#label(RUNS) is the last column, row[-1]
#features incldue from 1st columns till last but one column, row[1:-1] 
transformed_df = data.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[1:-1])))

#training and testing split ratio, seed value
TRAINING_DATA_RATIO = 0.7
RANDOM_SEED = 250
splits = [TRAINING_DATA_RATIO, 1.0 - TRAINING_DATA_RATIO]

#splitting the dataset into training and testing data
training_data, test_data = transformed_df.randomSplit(splits, RANDOM_SEED)

#print the number of rows in training and testing datasets
print("Number of training set rows: %d" % training_data.count())
print("Number of test set rows: %d" % test_data.count())


# In[ ]:


#to decide the best maxDepth value
from pyspark.mllib.tree import DecisionTree
from time import *

accuracy = []
depth = []

#calculating the accuracy for each maxDepth value varying from 5 to 30 in the steps of 5
for d in range(5,30,5):
    #store maxDepth value in depth list
    depth.append(d)
    
    #create a model with depth d by training it in traininig_data
    model = DecisionTree.trainClassifier(training_data, numClasses=8, 
            categoricalFeaturesInfo = {0:14,4:35},impurity='entropy', maxDepth=d, maxBins=35)
    
    #predict the output for rows of testing data 
    predictions = model.predict(test_data.map(lambda x: x.features))
    
    #compare the actual result and the predicted result to get the accuracy for depth d
    p = predictions.take(predictions.count())
    actual = test_data.map(lambda x:x.label)
    a = actual.take(actual.count())
    count = 0
    for i in range(len(a)):
        if(p[i]==a[i]):
            count = count+1

    #store the accuracy for depth d in accuracy list
    accuracy.append(count/len(a)*100)
    print("accuracy= ", count/len(a)*100, "for depth= ", d)
    
print(accuracy)
print(depth)


# In[ ]:


#plotting accuracy vs maxDepth graph
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1, figsize =(8,6))
ax.plot(depth,accuracy)
ax.set_xlabel('depth')
ax.set_ylabel('acccuracy')


# In[ ]:


#training the model for best value of maxDepth
from pyspark.mllib.tree import DecisionTree
from time import *

#to get the start time
start_time = time()

#parameters:
#training_data: is the data on which model gets trained
#numClasses: this should be more than the number of distinct target vaiable values
#categoricalFeaturesInfo: will take column_number which has categorial info and number of disctict values in theat column(categories)
#impurity: used to specify the impurity matrix used to create the model(can be entropy or gini)
#maxDepth: to specify maxDepth of the tree
#maxBins: to specify the number of bins used while splitting the tree based in features
#           (should be more than the number of max categories mentioned in the categoricalFeaturesInfo)
model = DecisionTree.trainClassifier(training_data, numClasses=8, 
        categoricalFeaturesInfo = {0:14,4:35},impurity='entropy', maxDepth=20, maxBins=35)
    
#to get the end time
end_time = time()

#calculate the time elapsed to train the model
elapsed_time = end_time - start_time
print("Time to train model: %.3f seconds" % elapsed_time)

#to the decision tree model created
#print(model.toDebugString())


# In[ ]:


#to get the prediction for each row of testing_data based on the model created
predictions = model.predict(test_data.map(lambda x: x.features))

#to put the predicted result into a list p 
p = predictions.take(predictions.count())

#to get the actual result from testing data
actual = test_data.map(lambda x:x.label)
#to put actual result into a list a
a = actual.take(actual.count())

#to find the accuracy of result by comparing the actual and predicted result
count = 0
for i in range(len(a)):
    if(p[i]==a[i]):
        count = count+1
print(count,"correct out of", len(a))
print("accuracy= ", count/len(a)*100)


# In[ ]:


import csv
import random
import os

#playersMapping: {player_name:player_number}
playersMapping = {}
#TeamMapping: {team_name:team_number}
TeamMapping = {}
#VenueMapping: {Venue:venue_number}
VenueMapping = {}
#bats_details: {batsman_name:batsman_number}
bats_details = {}
#bowl_details: {bowler_name:bowler_number}
bowl_details = {}

batord_team1 = []
batord_team2 = []
bowlord_team1 = []
bowlord_team2 = []

bat_team1 = {}
bat_team2 = {}
bowl_team1 = {}
bowl_team2 = {}

map_player = len(playersMapping.keys())
dic = {}
def preProcessing():

	#store teamname and its number in a dictionary TeamMapping by reading it from TeamMapping.csv
	#TeamMapping: {team_name:team_number}
	fp = open("/home/pratheeksha/Desktop/Phase3/InputCSVS/TeamMapping.csv",'r')
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
	    TeamMapping[i[0]]= i[1]
	fp.close()

	#store Venue and its number in a dictionary VenueMapping by reading it from VenueMapping.csv
	#VenueMapping: {Venue:venue_number}
	fp = open("/home/pratheeksha/Desktop/Phase3/InputCSVS/VenueMapping.csv",'r')
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
	    VenueMapping[i[0]]= i[1]
	fp.close()

	#store player_name and his number in a dictionary playersMapping by reading it from PlayerMapping.csv
	#playersMapping: {player_name:player_number}
	fp = open("/home/pratheeksha/Desktop/Phase3/InputCSVS/PlayerMapping.csv",'r')
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
		playersMapping[i[0]]= i[1]
	fp.close()

	#store batsman_name and his number in a dictionary bats_details by reading it from bats_details.csv
	#bats_details: {batsman_name:batsman_number}
	fp = open("/home/pratheeksha/Desktop/Phase3/InputCSVS/bats_details.csv","r")				
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
		#name, strikerate, average
		bats_details[i[0]] = [float(i[1]), float(i[2])]
	fp.close()

	#store bowler_name and his number in a dictionary bowl_details by reading it from bowl_details.csv
	#bowl_details: {bowler_name:bowler_number}
	fp = open("/home/pratheeksha/Desktop/Phase3/InputCSVS/bowl_details.csv","r")				
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
		#name, strikerate, economy
		bowl_details[i[0]] = [float(i[1]), float(i[2])]
	fp.close()

def getDetails():
	#reading batting order and bowlig order of both the teams from match.csv
	fp = open("/home/pratheeksha/Desktop/Phase3/InputCSVS/match.csv",'r')
	reader = csv.reader(fp)
	next(reader)
	for i in reader:
		batord_team1.append(i[0])
		batord_team2.append(i[1])
		bowlord_team1.append(i[2])
		bowlord_team2.append(i[3])

#to calculate the result of a particluar ball
#return (runs, wicket)
def calculate(batsman_name, non_striker, bowler_name, team_no):
	#dictionary which stores confidence values of striker and non-striker
	global dic
	global map_player

	#if new batsman-bolwer pair, add it to the dictionary and make confidence value as 1
	if((str(batsman_name)+str(bowler_name)) not in dic.keys()):
		dic[str(batsman_name)+str(bowler_name)] = 1
	else:
		#if his name is already present nultiply the old confidence with 0.85
		dic[str(batsman_name)+str(bowler_name)]  = dic[str(batsman_name)+str(bowler_name)]* 0.85

	var =dic[str(batsman_name)+str(bowler_name)]
	
	#getting striker name's correspoinding number.
	#if his name is not present assign new numebr to him
	if(batsman_name not in playersMapping.keys()):
		playersMapping[batsman_name] = map_player
		map_player = map_player + 1
	batsman1_no = playersMapping[batsman_name]
	
	#getting non-striker name's corresponding number
	#if his name is not present assign new numebr to him
	if(non_striker not in playersMapping.keys()):
		playersMapping[non_striker] = map_player
		map_player = map_player + 1
	batsman2_no = playersMapping[non_striker]

	#getting bowler name's corresponding number
	#if his name is not present assign new numebr to him
	if(bowler_name not in playersMapping.keys()):
		playersMapping[bowler_name] = map_player
		map_player = map_player + 1
	bowler_no   = playersMapping[bowler_name]

	#getting strike_rate and average of striker
	if(batsman_name not in bats_details.keys()):
		rand_num = random.randint(0,len(bats_details.keys())-1)
		bt1_str, bt1_avg = bats_details[list((bats_details.keys()))[rand_num]]
	else:
		bt1_str, bt1_avg = bats_details[batsman_name]

	#getting strike_rate and average of non-striker
	if(non_striker not in bats_details.keys()):
		rand_num = random.randint(0,len(bats_details.keys())-1)
		bt2_str, bt2_avg = bats_details[list((bats_details.keys()))[rand_num]]
	else:
		bt2_str, bt2_avg = bats_details[non_striker]

	#getting strike_rate and average of bowler
	if(bowler_name not in bowl_details.keys()):
		rand_num = random.randint(0,len(bowl_details.keys())-1)
		bo_str, bo_eco = bowl_details[list((bowl_details.keys()))[rand_num]]
	else:
		bo_str, bo_eco = bowl_details[bowler_name]

	#get team_no 
	if(team_no == 1):
		team = team1_no
	else:
		team = team2_no

	#feature which has to be passed as input to the model
	features = [ team, batsman1_no, batsman2_no, bowler_no, Venue_no, bt1_str, bt1_avg, bt2_str, bt2_avg, bo_eco, bo_str,var]

	#predicting the result for features
	prediction = model.predict(features)

	#if prediction is not 7(is not a wicket)
	if(prediction!=7.0):
		#return numnber if runs scored, which is first paramater
		return(int(prediction), 0)
	#if striker has got out, delete his entry from the dictionary which has confidence of the players playing 
	del dic[str(batsman_name)+str(bowler_name)]
	#return (0,1) indicating 0 runs and 1 wicket
	return (0,1)

def simulate_innings1(team_name):
	#list containing striker and non-striker names
	players = [batord_team1[0], batord_team1[1]]
	#remove striker and non-striker name from batting order of team1
	del batord_team1[0:2]

	#initialising variables
	bowlerindex = -1

	batsman_name= players[1]
	non_striker = players[0]
	
	total_team1 = 0
	num_balls = 0
	overs = 0.0   
	runs = 0.0
	wicket = 0
	total_wickets = 0

	filename = "simulation"
	
	#open csv in write mode
	with open(os.path.join(res_csvpath, filename)+".csv","w") as inputStream:
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
					batsman_name, non_striker = non_striker, batsman_name
			    	
			#predict runs and wickets for that particular ball		
			runs, wicket = calculate(batsman_name, non_striker, bowler_name, 1)

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
	
	return int(total_team1)

def simulate_innings2(team_name, total_team1):
	#list containing striker and non-striker names
	players = [batord_team2[0], batord_team2[1]]
	#remove striker and non-striker name from batting order of team1
	del batord_team2[0:2]
	bowlerindex = -1

	#initialising variables
	batsman_name= players[1]
	non_striker = players[0]

	total_team2 = 0
	num_balls = 0
	overs = 0.0   
	total_wickets = 0
	runs = 0.0
	wicket = 0

	filename = "simulation"

	#open csv in append mode
	with open(os.path.join(res_csvpath, filename)+".csv","a") as inputStream:
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
			runs, wicket = calculate( batsman_name, non_striker, bowler_name, 2)

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

	return int(total_team2)

if __name__ == "__main__":
	#path of the folder(simulated_csvs) where simulated csv get stored
	res_csvpath = "/home/pratheeksha/Desktop/Phase3"

	#if folder(simulated_csvs) doesn't exist, create one
	if not os.path.exists(res_csvpath):
		os.makedirs(res_csvpath)

	#function which stores all input csvs values into dictionaries
	preProcessing()
	#to get details
	getDetails()

	#get team numbers from teamnames, venue number from venue name
	team1_name = "RCB"
	team1_no = TeamMapping[team1_name]
	team2_name = "KKR"
	team2_no = TeamMapping[team2_name]
	Venue = "Eden Gardens"
	Venue_no = VenueMapping[Venue]

	#simuation for first innings
	team1_total = simulate_innings1(team1_name)
	#simulation for second innings
	team2_total = simulate_innings2(team2_name, team1_total)

	#to print the final scores of both teams 
	print("team1 total: ",team1_total,"\nteam2 total: ", team2_total)
	#to print whicb team won
	if(team1_total>team2_total):
		print(team1_name,"won!")
	elif(team2_total>team1_total):
		print(team2_name,"won!")
	else:
		print("DRAW")

