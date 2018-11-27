# Web scraping code which gets the detail of all player (Player profile)

from lxml import html
import requests
import urllib.request
from bs4 import BeautifulSoup

# getting the data for batsman
# Look for the appropirate link for the bowler data
start_page=requests.get("http://stats.espncricinfo.com/indian-premier-league-2016/engine/records/averages/batting.html?id=11001;type=tournament")
tree=html.fromstring(start_page.text)
playerName = tree.xpath('//td[@class="left"]/a/text()')
playerProfile = tree.xpath('//tr[@class="data2"]/td/text()')

for i in playerName:
	if i=="Twenty20":
		playerName.remove(i)
k = 0
a = []
l = []

for i in playerProfile:
	if i!='':
		l.append(i)
		k+=1
		if k == 13:     #13 attributes if batting ,14 if bowling
			a.append(l)
			l = []
			k=0

for i in range(len(a)):
	a[i].insert(0,playerName[i])


# Uncomment one of the part based on what data is required bowler or batman.

# For Bowler

# p =  open("Bowl.csv","w") 
# writer  = csv.writer(p)
# writer.writerow(['Player','Mat','Inns','Overs','Mdns','Runs','Wkts','BBI','Ave','Econ','SR','4','5','Ct','St'])
# for i in a:
# 	writer.writerow(i)

# For Batsman

# p =  open("Bat.csv","w") 
# writer  = csv.writer(p)
# writer.writerow(['PLayer','Mat','Inns','NO','Runs','HS','Ave','BF','SR','100','50','0','4s','6s']
# for i in a:
# 	writer.writerow(i)