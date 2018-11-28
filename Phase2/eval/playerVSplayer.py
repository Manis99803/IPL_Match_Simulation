# Computing player vs player statistics by parsing over all the IPL yaml files downloaded from the cricsheet.org

import yaml
import re
import csv
import os


playerStatistics = {}	# Player statistics is the ditionary which will have all the player vs player statistics.
playerList = []
ok = 1
def probabilityFunction(fileName):
	with open(fileName) as outputstream:
		newSubList = []
		data = yaml.dump(yaml.load(outputstream))  			# yaml file data is stored in "data" variable and all the which is in string format
		data = str(data)
		finalDataList = []
		pattern = re.compile(r'dates:(.*)')					
		date = pattern.findall(data)   			#Format : [2005-06-13]
		date = date[0][2:(len(date[0])-1)] 		#Removing all the brackets as the format is a string and not list	
		date = date.split("-")
		if ok == 1  :							

			# using regex we obtain the data required 
			pattern = re.compile(r'\d.\d:|\d\d.\d:|batsman:.\w+.\w+| bowler:.\w+.\w+|non_striker:.\w+.\w+|batsman:.\d|extras:.\d|wicket:|kind:.\w+|player_out:.\w+.\w+') 
			getData = pattern.findall(data)

			# getting the ball by data and making it a sublist and storing it in finalDataList
			for i in range(len(getData)):
					try:
							(float(getData[i][0:len(getData[i])-1]))
							newSubList=[]
							finalDataList.append(newSubList)
							newSubList.append(float(getData[i]))
					except:
						
						newSubList.append(getData[i])		
			for i in finalDataList:
					playerName = i[1].split(":")[1].rstrip().lstrip()
					bowlerName = i[2].split(":")[1].rstrip().lstrip()
					runs = i[4].split(":")[1].rstrip().lstrip()
					
					# If the length of the sublist is greater than 6 which means a wicket is fallen on that ball.
					if len(i)>6:
						playerOut = i[8].split(":")[1].rstrip().lstrip()
						outType = i[7].split(":")[1].rstrip().lstrip() 
						if playerOut not in playerStatistics:
							playerStatistics[playerOut] ={}
							playerStatistics[playerOut].update({bowlerName:{0:[0,0],1:[0,0],2:[0,0],3:[0,0],4:[0,0],6:[0,0],'total':[],'wicket':0}})
							if int(runs) == 0:
								playerStatistics[playerOut][bowlerName][0][0] += 1
							elif int(runs) == 1:
								playerStatistics[playerOut][bowlerName][1][0] += 1
							elif int(runs) == 2:
								playerStatistics[playerOut][bowlerName][2][0] += 1
							elif int(runs) == 3:
								playerStatistics[playerOut][bowlerName][3][0] += 1
							elif int(runs) == 4: 
								playerStatistics[playerOut][bowlerName][4][0] += 1
							else:
								playerStatistics[playerOut][bowlerName][6][0] += 1
							playerStatistics[playerOut][bowlerName]['total'].extend([int(runs),int(1)])
							playerStatistics[playerOut][bowlerName]['wicket'] = 1
						
						else:
							if bowlerName not in playerStatistics[playerOut]:
								playerStatistics[playerOut].update({bowlerName:{0:[0,0],1:[0,0],2:[0,0],3:[0,0],4:[0,0],6:[0,0],'total':[],'wicket':0}})
								if int(runs) == 0:
									playerStatistics[playerOut][bowlerName][0][0] += 1
								elif int(runs) == 1:
									playerStatistics[playerOut][bowlerName][1][0] += 1
								elif int(runs) == 2:
									playerStatistics[playerOut][bowlerName][2][0] += 1
								elif int(runs) == 3:
									playerStatistics[playerOut][bowlerName][3][0] += 1
								elif int(runs) == 4: 
									playerStatistics[playerOut][bowlerName][4][0] += 1
								else:
									playerStatistics[playerOut][bowlerName][6][0] += 1
								playerStatistics[playerOut][bowlerName]['total'].extend([int(runs),int(1)])
								playerStatistics[playerOut][bowlerName]['wicket'] = 1
							
							else:
								
								if int(runs) == 0:
									playerStatistics[playerOut][bowlerName][0][0] += 1
								elif int(runs) == 1:
									playerStatistics[playerOut][bowlerName][1][0] += 1
								elif int(runs) == 2:
									playerStatistics[playerOut][bowlerName][2][0] += 1
								elif int(runs) == 3:
									playerStatistics[playerOut][bowlerName][3][0] += 1
								elif int(runs) == 4: 
									playerStatistics[playerOut][bowlerName][4][0] += 1
								else:
									playerStatistics[playerOut][bowlerName][6][0] += 1
								playerStatistics[playerOut][bowlerName]['total'][0] += (int(runs))
								playerStatistics[playerOut][bowlerName]['total'][1]	+= (int(1))
								playerStatistics[playerOut][bowlerName]['wicket'] += 1
					else:
						if playerName not in playerStatistics:
							playerStatistics[playerName] ={}
							playerStatistics[playerName].update({bowlerName:{0:[0,0],1:[0,0],2:[0,0],3:[0,0],4:[0,0],6:[0,0],'total':[],'wicket':0}})
							if int(runs) == 0:
								playerStatistics[playerName][bowlerName][0][0] += 1
							elif int(runs) == 1:
								playerStatistics[playerName][bowlerName][1][0] += 1
							elif int(runs) == 2:
								playerStatistics[playerName][bowlerName][2][0] += 1
							elif int(runs) == 3:
								playerStatistics[playerName][bowlerName][3][0] += 1
							elif int(runs) == 4: 
								playerStatistics[playerName][bowlerName][4][0] += 1
							else:
								playerStatistics[playerName][bowlerName][6][0] += 1
							playerStatistics[playerName][bowlerName]['total'].extend([int(runs),int(1)])
						
						else:
							if bowlerName not in playerStatistics[playerName]:
								playerStatistics[playerName].update({bowlerName:{0:[0,0],1:[0,0],2:[0,0],3:[0,0],4:[0,0],6:[0,0],'total':[],'wicket':0}})
								if int(runs) == 0:
									playerStatistics[playerName][bowlerName][0][0] += 1
								elif int(runs) == 1:
									playerStatistics[playerName][bowlerName][1][0] += 1
								elif int(runs) == 2:
									playerStatistics[playerName][bowlerName][2][0] += 1
								elif int(runs) == 3:
									playerStatistics[playerName][bowlerName][3][0] += 1
								elif int(runs) == 4: 
									playerStatistics[playerName][bowlerName][4][0] += 1
								else:
									playerStatistics[playerName][bowlerName][6][0] += 1
								playerStatistics[playerName][bowlerName]['total'].extend([int(runs),int(1)])
							else:
								if int(runs) == 0:
									playerStatistics[playerName][bowlerName][0][0] += 1
								elif int(runs) == 1:
									playerStatistics[playerName][bowlerName][1][0] += 1
								elif int(runs) == 2:
									playerStatistics[playerName][bowlerName][2][0] += 1
								elif int(runs) == 3:
									playerStatistics[playerName][bowlerName][3][0] += 1
								elif int(runs) == 4: 
									playerStatistics[playerName][bowlerName][4][0] += 1
								else:
									playerStatistics[playerName][bowlerName][6][0] += 1
								playerStatistics[playerName][bowlerName]['total'][0] += int(runs)
								playerStatistics[playerName][bowlerName]['total'][1] += int(1)

			
if __name__=="__main__":

	path = "/home/manish/manish/Manish/Documents/5th_Sem/Big_Data/Project/ipl"
	supported_formats = ('.yaml')
    
    #list containing all the paths of yaml files
	path_list = [os.path.join(path, fname) for fname in os.listdir(path) if fname.lower().endswith(supported_formats)]   
	for i in path_list:
		probabilityFunction(i)

	probabilityList = ["Batsman","Bowler","P(0)","P(1)","P(2)","P(3)","P(4)","P(6)","P(W)"]
	filePointer = open("probabilty.csv","a")
	writer = csv.writer(filePointer)
	writer.writerow(probabilityList)

	for key,value in playerStatistics.items():
		for i,j in value.items():
			counter = 0													# Counter ,so that the probabilty is calculated only for the runs 
			for m in list(j.keys()):
				if counter!=6:											# Bcos we have 6 types : 0,1,2,3,4,6 ,counter!=6 bcos counter is initialised to 0 and not 1
					j[m][1] = (j[m][0]/j['total'][1])
					counter+=1

	# Storing all the data player vs player data in a csv file.
	filePointer = open("probabilty.csv","a")
	writer = csv.writer(filePointer)
	for key,value in playerStatistics.items():
		for i,j in value.items():
			writer.writerow([key,i,j[0][1],j[1][1],j[2][1],j[3][1],j[4][1],j[6][1],j['wicket']/j['total'][1]])	
