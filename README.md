# IPL ANALYSIS
## Simulation of IPL matches using Big Data techniques

### Introduction
Our project is IPL analysis and simulation using big data techniques.
We have implemented the simulation of matches using two different approaches:
#### 1) Clustering Approach
This involves predicting the score based on a random number generated.
#### 2) Decision Trees
Decision Trees  are a non-parametric supervised learning method used for classification and regression. The goal is to create a model that predicts the value of a target variable by learning simple decision rules inferred from the data features.
The technologies used in our project are:

1)Hadoop
2)Spark
3)Python
4)Machine learning techniques like K-means clustering and decision trees.

### Dataset
+ inp_csv:
	- bats_centroids.csv : File which has centroids of all the batsman cluster *Format* : Cluster number , Average, Strike rate

	- bowl_centroids.csv : File which has centroids of all the bowler cluster
	 *Format* : Cluster number , Economy, Strike rate

	- bats_res.csv : File which has details of to which cluster the batsman belongs.
	*Format* : Batsman name, Cluster number

	- bowl_res.csv : File which has details of which cluster the bowler belongs to.
	*Format* : Bowler name, Cluster number

	- bats_details.csv : File which has average and strike rate of every batsman *Format* : Batsman name, Average, Strike rate

	- bowl_details.csv : File which has economy and strike rate of every bowler
	 *Format* : Bowler name, Economy, Strike rate

	- clsVscls.csv : File which has the cluster vs cluster probability of runs scoring.
	 *Format* : Cluster 1,Cluster 2, prob(0), prob(1), prob(2), prob(3), prob(4), prob(6), prob(W)

	- Probability.csv or Updated  Probabitity.csv : File which has player vs player probability statistics.
	 *Format* : Batsman name, Bowler name, prob(0), prob(1), prob(2), prob(3), prob(4), prob(6), prob(W)

	- FinalPLayerData.csv : File with player info.
	 *Format* : Player name, Batting Average,Bowling Average 

+ simulated_csv:

	Folder which has file for every match simualated.

+ test_matches:
	
	Input file for the simulation

Phase 3:
	Data set used for the phase
+ Final_Data_Set : The one used for the decision tree.
	 Format : Team number, Batsman 1 number, Batsman 2 number,Bowler number,Venue number, Batsman 1 strike rate, Batsman1 average, Batsman2 strike rate, Batsman2 average, Bowler Economy, Bowler Strike rate, Confidence value, Runs

+ Player vs player info data is taken and addtional attributes like strike rate,average, venue and confidence are added and the data set is created for the decision tree.

	- Confidence value is updated every ball by multiplying it with a 0.85 factor when the same pair is encountered
	
	- Every categorical data , textual data is converted to a number

### Implementation
The entire project has been implemented in three different phases:

##### PHASE 1:
 Clustering of Batsmen and Bowlers using K-Means algorithm

Considering the optimal K-value as 10,we have grouped the batsmen and bowlers into 10 different clusters based on the following attributes:

Batsmen: Average,strike-rate
Bowlers:Economy,strike-rate


##### PHASE 2:
Simulate match using random number and cumulative probability for runs and wicket.
We simulate the match using cluster data obtained from phase 1.

  
##### PHASE 3:
Simulating match using Decision Trees:

The decision trees are used for simulating the match and predict the outcome of the match by predicting the runs and wickets using mllib.

### Deployment
This project has been implemented using python.

Entire project has been executed in jupyter notebook.

Phase 1,3 involves usage of **pyspark** which has been included in jupyter notebook.
#### Contributers
Manish Soni

Pragya Agrawal

Pratheeksha D R

R P Shreya Reddy