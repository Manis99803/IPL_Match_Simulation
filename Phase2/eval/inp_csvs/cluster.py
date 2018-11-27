import csv
filePointer = open("bowl_res.csv")
reader = csv.reader(filePointer)
next(reader)
bowlerClusterDictionary = {}
for i in reader:
	if i[1] not in bowlerClusterDictionary:
		bowlerClusterDictionary[i[1]] = 1
	else:
		bowlerClusterDictionary[i[1]] += 1
print(bowlerClusterDictionary)
