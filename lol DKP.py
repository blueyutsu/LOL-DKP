#Created by Tasman Daengdej, last edited 02/07/2018

import pycurl
import certifi
from io import BytesIO
import ast
opentext = open("DKPvars", "r")
lossdict = ast.literal_eval(opentext.read())

#A dictionary which will store the matchlist for each person using data from the RIOT API
dic={"taslst":[], "roblst":[], "hadlst":[], "marclst":[], "arsharlst":[], "lachielst":[]}

#a dictionary with each person as items and their net DKP loss as values, (currently disabled as we're reading from a text file)
#lossdict={"tasloss":0, "hadloss":0, "robloss":0, "marcloss":0, "arsharloss":0, "lachieloss":0}

#This function returns the net DKP of a person given lst (the value assigned to the item "matches" from the riot api)
#and optionally given dkploss (the amount of lost DKP due to bidding)
def getdkp(lst, dkploss=0):
    count=0
    for game in lst:
        if int(game["timestamp"])>1530467286271:
            count+=1
        else:
            break
    return ("DKP: " + str((count*50)-int(dkploss)))

#This block of code auto generates all the URLs for accessing the match data from the Riot API
key=input("Input api key:")
names=[("Tas", 200075750, "taslst", "tasloss"), ("Rob", 200051491, "roblst", "robloss"), ("Hadleigh", 200892109, "hadlst", "hadloss"), ("Marc", 200864612, "marclst", "marcloss"), ("Arshar", 200307228, "arsharlst", "arsharloss"), ("Lachie", 200854432, "lachielst", "lachieloss")]
for name in names:
    print("{} match list: https://oc1.api.riotgames.com/lol/match/v3/matchlists/by-account/{}?api_key={}".format(str(name[0]), str(name[1]), str(key)))
print(200*"-")
print()

#Communicates with riot api to get matchlist data
for name in names:
    AccountId=name[1]
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,
             "https://oc1.api.riotgames.com/lol/match/v3/matchlists/by-account/{}?api_key={}".format(str(AccountId),
                                                                                                     str(key)))
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    matchlist = buffer.getvalue()
    matchlist = matchlist.decode('iso-8859-1')
    matchlist = ast.literal_eval(matchlist)
    truelst=matchlist["matches"]
    dic[name[2]]=truelst

#nloss is the name of the bid victor and loss is the amount of DKP lost in the winning bid
nloss=input("Input name of bid victor (Tas, Rob, Hadleigh, Marc, Arshar, Lachie): ")
loss=input("Input amount of DKP loss (0 if just checking DKP): ")


for name in names:
    #checks for invalid DKP inputs
    if not loss.isdigit():
        print()
        print(20 * "! ")
        print()
        print("INVALID DKP AMOUNT, PLEASE USE A NUMBER")
        print()
        print(20 * "! ")
        print()
        break
    #checks for invalid name inputs
    if str(nloss).lower() not in ("tas", "rob", "hadleigh", "marc", "arshar", "lachie"):
        print()
        print(50*"! ")
        print()
        print("INVALID NAME, MAKE SURE THE SPELLING IS CORRECT: (Tas, Rob, Hadleigh, Marc, Arshar, Lachie)")
        print()
        print(50 * "! ")
        break
    #increases the net lost DKP of the winning bidder to the new amount
    if str(nloss).lower() in name[0].lower():
        lossdict[name[3]] += float(loss)
        break

print()
print("Current DKP amounts")
#prints the current DKP amounts for everyone
for name in names:
    print("{} {}".format(str(name[0]), str(getdkp(dic[name[2]], lossdict[name[3]]))))
print()
print(200 * "-")

text_file = open("DKPvars", "w")
text_file.write(str(lossdict))
text_file.close()
