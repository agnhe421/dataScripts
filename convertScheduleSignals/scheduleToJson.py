import json
from pathlib import Path

def isNotEmpty(s):
    return bool(s and s.strip())

def isData(s):
    return bool(s.find("*") == -1)

def findYear(s):
    if (s.find("***") == -1):
    	return False
    else:
    	return	True

def updateDay(s):
	dayInt = int(s)
	dayString =""

	if(dayInt == 365):
		dayString == "001"
		
	elif dayInt >= 100:
		dayString = str(dayInt + 1)

	elif dayInt >= 9 and dayInt < 100:
		dayString = str("0" + str(dayInt + 1))
	
	elif (dayInt < 9):
		dayString = str("00" + str(dayInt + 1))

	return dayString

def updateYear(year):
	yearInt = int(year)
	yearInt = yearInt + 1
	yearString = str(yearInt)
	return yearString


def findDirection(s):
	#get equipmentlist to decide if uplink/downlink, then delete it
	equipmentString = s.replace(";", "")
	equipmentListObj = equipmentString.split(",");
	
	#deal with uplink/downlink
	linkString =''
	isDownlink = False
	isUplink = False

	for equipment in equipmentListObj:
		if (equipment == 'UPL'):
	 		isUplink = True;
		if (equipment == 'RRPA' or equipment == 'RRPB' or equipment == 'TLPB' or equipment == 'TLPA'):
	 		isDownlink = True;
	if(isDownlink and isUplink):
	 		linkString += 'both'
	elif(isUplink):
	 		linkString += 'uplink'	
	elif(isDownlink):
	 		linkString += 'downlink'					
	else :
	 		linkString = "None"	
	
	return linkString


directory_in_str = "C://Users//openspace//Agnes//convertToJSON//convertScheduleSignals//data"
pathlist = Path(directory_in_str).glob('**/*.csv')
for path in pathlist:
	path_in_str = str(path)
	filename = path_in_str

	DISHES = []
	DAYS = []
	BOT = []
	EOT = []
	SPACECRAFT = []
	WRKCAT = []
	EQUIPMENT = []
	DLT = 0

	dataObj = {}
	data = []
	output = {}

	infile = open(filename, 'r')
	lines = [line for line in infile] 
	for x in range (0, len(lines)):
		if findYear(lines[x]):
			year = str("20" + lines[x][43:46].strip())
			yearChange = str("20" + lines[x][55:58].strip())
			newYear = False

			if(lines[x][43:46].strip() != lines[x][55:58].strip()):
				year = str("20" + lines[x][43:46].strip())
				yearChange = str("20" + lines[x][55:58].strip())
				newYear = True
				#print(lines[x][55:58].strip())


		if isData(lines[x]):
			if(lines[x][72:75] == '1A1'):
				WRKCAT.append(lines[x][72:75])
				if(isNotEmpty(lines[x][0:4])):
					#Make sure we can handle new years in the same week
					if(newYear == True):
						if( lines[x][0:2].strip() == "3"):
							DAYS.append(str( year + "-" + lines[x][0:4].strip()))
						else: 
							DAYS.append(str( yearChange + "-" + lines[x][0:4].strip()))
					else: 
						DAYS.append(str( year + "-" + lines[x][0:4].strip()))

				if((lines[x][10:11]).isdigit()):
						BOT.append(str(lines[x][10:12] + ":" + lines[x][12:14] ))
				if((lines[x][15:16]).isdigit()):
						EOT.append(str(lines[x][15:17] + ":" + lines[x][17:19] ))
				if(lines[x][26:29] == 'DSS'):
					DISHES.append(lines[x][26:32])

				if(isNotEmpty(lines[x][33:36])):
					SPACECRAFT.append(lines[x][34:38].strip())
			
			if((lines[x][10:11]).isalpha()):
				EQUIPMENT.append(findDirection(lines[x][10:50].strip()))
				

	for x in range(0, len(DISHES)):
		
		if(int(EOT[x][0:2] + EOT[x][3:5]) < int(BOT[x][0:2] + BOT[x][3:5])):
			day = updateDay(DAYS[x][5:8])
			if(DAYS[x][5:8] == "365"):
				year = updateYear(DAYS[x][0:4])
				day = "001"
				print(day)
				EOT[x] = str(year + '-' + day + "T"  + EOT[x])
			else:
				EOT[x] = str(DAYS[x][0:5] + day + "T"  + EOT[x])
		else: 
			EOT[x] = str(DAYS[x] + "T" + EOT[x])

		BOT[x] = str(DAYS[x] + "T" + BOT[x])
		DISHES[x] = DISHES[x].replace("-", "")

		if(SPACECRAFT[x] == "VGR1" or SPACECRAFT[x] == "VGR2" or SPACECRAFT[x] == "MRO" or SPACECRAFT[x] == "STA"):
			if(EQUIPMENT[x] != "None"):
				dataObj =  {'facility': DISHES[x], 
								'bot' : BOT[x], 
				 				'eot' : EOT[x], 
				 				'projuser' : SPACECRAFT[x],
				 				'direction' : EQUIPMENT[x],
				 				'DLT' : DLT } 

				data.append(dataObj)
				

		if(x+1 < len(DAYS) and DAYS[x] != DAYS[x+1]):
				output["Signals"] = data
				outputFilename = open(str("parsed/" + DAYS[x])+ "T" + '.json', 'w')
				json.dump(output, outputFilename, indent=4)
				data.clear()

		elif(x == len(DAYS) -1):
				output["Signals"] = data
				outputFilename = open(str("parsed/" + DAYS[x])+  "T" + '.json', 'w')
				json.dump(output, outputFilename, indent=4)	
				data.clear()
			