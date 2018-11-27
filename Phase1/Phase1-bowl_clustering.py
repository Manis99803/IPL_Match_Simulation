
# coding: utf-8

# In[ ]:


#reading from hdfs

from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql import SQLContext

#creating spark session
sparkSession = SparkSession.builder.appName("bowler-cluster").getOrCreate()

#if csv has header
#loading bowl_details.csv from hdfs 
df_load = sparkSession.read.csv('hdfs://localhost:9000/input/bowl_details.csv', header=True)

#renaming column names
df_load = df_load.withColumnRenamed("bowler", "player_name")
df_load = df_load.withColumnRenamed("economy", "economy")
df_load = df_load.withColumnRenamed("strike_rate", "strike_rate")

#use this if header is not present
'''
df_load = sparkSession.read.csv('hdfs://localhost:9000/input/bowl_details.csv', header=False)
#df_load = df_load.withColumnRenamed("_c0", "player_name")
#df_load = df_load.withColumnRenamed("_c1", "average")
#df_load = df_load.withColumnRenamed("_c2", "strike_rate")
'''
#to see the dataframe format
df_load.show()
print(type(df_load))


# In[ ]:


from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col , column
from pyspark.sql.functions import *

#fill null values with 0 
df_load = df_load.na.fill({'economy': '0'})
df_load = df_load.na.fill({'strike_rate': '0'})

#convert all strings to double
df_load = df_load.withColumn("economy", col("economy").cast("double"))
df_load = df_load.withColumn("strike_rate", col("strike_rate").cast("double")))

#form a feature column by joining average and strike_rate column
vecAssembler = VectorAssembler(inputCols=["strike_rate","economy"], outputCol="features")

#to add feature column to the original dataframe
new_df = vecAssembler.transform(df_load)

#to see the new dataframe
new_df.show()


# In[ ]:


#create new dataframe which has only player_name and features as columns
df_kmeans = vecAssembler.transform(df_load).select('player_name', 'features')

#to see the input format that will be given to k-means clustering
df_kmeans.show()


# In[ ]:


#to decide the best k value
import numpy as np
from pyspark.ml.clustering import KMeans

#compute the cost of clustering output by varying k-values from 2 to 19 
cost = np.zeros(20)
for k in range(2,20):
    kmeans = KMeans().setK(k).setSeed(50).setFeaturesCol("features")
    model = kmeans.fit(df_kmeans)
    cost[k] = model.computeCost(df_kmeans) 


# In[ ]:


#plotting cost vs k-values to know which k value to choose
get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyspark import SparkContext
from pyspark.ml.clustering import KMeans
from sklearn.datasets.samples_generator import make_blobs
from mpl_toolkits.mplot3d import Axes3D


fig, ax = plt.subplots(1,1, figsize =(8,6))
ax.plot(range(2,20),cost[2:20])
ax.set_xlabel('k')
ax.set_ylabel('cost')


# In[ ]:


#optimal k value
k = 10

#fit the model with dataset
kmeans = KMeans().setK(k).setSeed(1).setFeaturesCol("features")
model = kmeans.fit(df_kmeans)

#to get batsman cluster's centroids
centers = model.clusterCenters()

print("Cluster Centers: ")
for center in centers:
    print(center)


# In[ ]:


#dataframe to see the cluster to which a batsman belongs to
#select player_name and prediction columns from the kmeans output dataframe
transformed = model.transform(df_kmeans).select('player_name', 'prediction')
rows = transformed.collect()

df_pred = sqlContext.createDataFrame(rows)
df_pred.show()


# In[ ]:


#storing output into hdfs in csv format
#bowl_clusters.csv : bowler_name, cluster_number

df = df_pred
df = df.withColumn("player_name", col("player_name").cast("string"))
df = df.withColumn("prediction", col("prediction").cast("string"))

df.write.csv('hdfs://localhost:9000/input/bowl_clusters.csv')
print("saved")


# In[ ]:


#add prediction(cluster number) column to the original dataframe
#by joining output dataframe(df_pred) and original(new_df) based on player_name 
df_pred = df_pred.join(new_df, 'player_name')
df_pred.show()

#converting spark dataframe into pandas dataframe to plot points in each cluster
pddf_pred = df_pred.toPandas().set_index('player_name')
pddf_pred.head()


# In[ ]:


#plot to see how the datapoints belonging to each cluster
threedee = plt.figure(figsize=(15,10)).gca(projection='3d')

threedee.scatter(pddf_pred.economy, pddf_pred.strike_rate, c=pddf_pred.prediction)
threedee.set_xlabel('economy')
threedee.set_ylabel('strike_rate')
threedee.set_zlabel('prediction')
plt.show()

