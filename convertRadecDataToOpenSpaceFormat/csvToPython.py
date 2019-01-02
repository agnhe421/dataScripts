import csv
import json
from collections import defaultdict
from pathlib import Path


localPath = "C:/Users/openspace/Agnes/convertToJSON/convertRadecDataToOpenSpaceFormat/"
generatedDataDir = "parsed/"
generatedExtension = ".json"
spacecraftName = "NHPC_TEST"
dataDir = "data/"
dataExtension = ".dat"

# Generated filename as date, Format: YYYY-DDDTHH
nameFormat = ""
hours = []
nameFormatList = []
positions = {}
data = []
oneHourData = []


dataPath = dataDir + spacecraftName + dataExtension

with open(dataPath) as f:
	reader = csv.DictReader(f, fieldnames=['TimeStamp', 'AzUp', 'ElUp', 'RngUp', 'AzDn', 'ElDn', 'RngDn', 
		'RAUp', 'DecUp', 'GeoRngUp', 'RADn', 'DecDn', 'GeoRngDn', 'ULT', 'RTLT_Up', 'XADop', 'DLT', 'RTLT_Dn', 'OneWayDop', 'TwoWayDop']) 
	for row in reader:
		del row['AzUp']
		del row['ElUp']
		del row['RngUp']
		del row['AzDn']
		del row['ElDn']
		del row['RngDn']
		del row['RAUp'] 
		del row['DecUp']
		del row['GeoRngUp']
		del row['ULT']
		del row['RTLT_Up']
		del row['XADop']
		#del row['DLT']
		del row['OneWayDop']
		del row['TwoWayDop']
		del row['RTLT_Dn']

		#print(row['TimeStamp'])
		row['RADn'] = float(row['RADn'])
		row['DecDn'] = float(row['DecDn'])
		row['GeoRngDn'] = float(row['GeoRngDn'])
		row['DLT'] = float(row['DLT'])
		row['TimeStamp'] = row['TimeStamp'][0:14]
		
		#Create our filename from the timestamp
		nameFormat = row["TimeStamp"][0:11]
		nameFormatList.append(nameFormat)
		#print(name)
		hour = row["TimeStamp"][9:11]
		hours.append(int(hour))

		data.append(row)

for i in range(0, len(data)):
	if(i+1 < len(nameFormatList) and nameFormatList[i] == nameFormatList[i+1]):
		oneHourData.append(data[i])
	elif (len(oneHourData) > 0):

		fileNameString = str( localPath + generatedDataDir + spacecraftName + "/" + names[i] + generatedExtension )
		my_file = Path(fileNameString)
		if my_file.is_file():
			#print("File already exists for" + fileNameString)

		outputData = open(fileNameString, 'w')
		positions["Positions"] = oneHourData
		json.dump(positions,outputData, indent=4)
		del oneHourData[:]
