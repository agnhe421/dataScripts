import json
#import csv
from pathlib import Path
# -------------------------------- TO EDIT ---------------------------------------#
#The local path where the script and data folders are located
localPath = "C://Users//openspace//Agnes//convertToJSON//addLightTravelTimeToSignals"
# A list of all the spacecrafts that we have positioning data for
spacecraftList = ["NHPC"]
# ---------------------------------------------------------------------------------#
#The dates for the signals stored in a vector
signalDates  = []
signalDir = localPath + "//signalData//"
radecDir = localPath + "//radecData//"

#the date of signalfile has the format 'YYYY-DDDT.json'
idxStartDateStr = -14 #counting from end of path
idxStartFileExtension = -5 #counting from end of path
fileExtensionSignal = '.json'
timeStrLength = 9

#the date of radec file has the format 'YYYY-DDDTHH.json'
fileExtensionRadec = '.json'


pathlistSignal = Path(signalDir).glob('**/*'+fileExtensionSignal)
#pathlistRadecData = Path(radecDir).glob('**/*'+fileExtensionRadec)

#print(pathlistRadecData)

for signalpath in pathlistSignal:
	signalPathStr = str(signalpath)
	
	signalDates.append(signalPathStr[idxStartDateStr:idxStartFileExtension])

#loop through all signal files
for currentSignalDate in range (0, len(signalDates)):
	with open(str(signalDir + signalDates[currentSignalDate] + fileExtensionSignal), 'r+') as signalFile:
		signalData = json.load(signalFile)
		
		#loop through all signals in the file
		for currentSignal in range( 0, len(signalData["Signals"])):
			spacecraft = signalData["Signals"][currentSignal]["projuser"]
			
			#check for matching spacecraft from our list
			for idx in range( 0, len(spacecraftList)):
				#if the spacecraft is in our list
				if(spacecraftList[idx] == spacecraft):
					timestampSignal = signalData["Signals"][currentSignal]["bot"][0:timeStrLength]
					radecDataFolder = radecDir + spacecraft + "//"
					radecPathList = Path(radecDataFolder).glob('**/*'+fileExtensionRadec)
					foundData = False
					firstLightTravelTimeInFile = 0
					for radecFilePath in radecPathList:
						defaultPath = radecFilePath
					    # because path is object not string
						pathStr = str(radecFilePath)
						if(pathStr.find(timestampSignal) != -1):
							foundData = True
							#print("For time: " + timestampSignal + "and spacecraft: " + spacecraft)
							#print(pathStr)
							with open(pathStr, 'r+') as spacecraftFile:
								radecPositionData = json.load(spacecraftFile)
								#get first position value for the matching day, and take its light travel time
								firstLightTravelTimeInFile = radecPositionData["Positions"][0]["DLT"]
								#print(firstLightTravelTimeInFile)
							break#break for loop when we get a match for the same day


					if foundData == True:
						print("Found lighttravelTime: "+ str(firstLightTravelTimeInFile) +", SignalTime: " + timestampSignal + ", Spacecraft: " + spacecraft)
						print("From file: " + pathStr)
						signalData["Signals"][currentSignal]["DLT"] =  float(firstLightTravelTimeInFile)
					#break #if statement
					else:
						with open(defaultPath, 'r+') as spacecraftFile:
								radecPositionData = json.load(spacecraftFile)
								firstLightTravelTimeInFile = radecPositionData["Positions"][0]["DLT"]
						print("Default DLT from path: " + str(defaultPath) + " DLT = " +  str(firstLightTravelTimeInFile))
						signalData["Signals"][currentSignal]["DLT"] =  float(firstLightTravelTimeInFile)


		signalFile.seek(0)
		json.dump(signalData, signalFile, indent = 4)
		signalFile.truncate()						
