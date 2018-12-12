import json
import csv
from pathlib import Path
from bisect import bisect_left
from astropy.time import Time

myOldList = []
testSignal = []


dataDict = {}
directory_in_str = "C://Users//openspace//Agnes//convertToJSON//addLightTravelTimeToSignals//signalData"
pathlist = Path(directory_in_str).glob('**/*.json')

#print(pathlist)
for path in pathlist:

		with open('radecData/VGR1-5years.dat') as f:
			reader = csv.DictReader(f, fieldnames=['TimeStamp', 'AzUp', 'ElUp', 'RngUp', 'AzDn', 'ElDn', 'RngDn', 'RAUp', 'DecUp', 'GeoRngUp', 'RADn', 'DecDn', 'GeoRngDn', 'ULT', 'RTLT_Up', 'XADop', 'DLT', 'RTLT_Dn', 'OneWayDop', 'TwoWayDop']) 

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
				del row['RTLT_Dn']
				del row['OneWayDop']
				del row['TwoWayDop']
				del row['RADn']
				del row['DecDn']
				del row['GeoRngDn']

				path_in_str = str(path)

				with open(path_in_str) as data_file:    
					data = json.load(data_file)
					signal = (data["Signals"])
					
					for i in range(0, len(signal)):
						if(signal[i]["bot"][0:8] in row['TimeStamp'][0:8]): 
							if( signal[i]["projuser"] == "VGR1"):
								signal[i]["DLT"] = row['DLT']	
								testSignal.append(signal[i])
							else:
								testSignal.append(signal[i])

					
startIndex = 0;
for j in range(0, len(testSignal)):
		if (j+1 < len(testSignal) and (testSignal[j]["bot"][0:8] != testSignal[j+1]["bot"][0:8])):
			filename = str("output/" + testSignal[j]["bot"][0:9]+'.json' )
			outputData = open(filename, 'w')
			print(filename)
			dataDict["Signals"] = testSignal[startIndex:j+1];
			json.dump(dataDict, outputData, indent=4)
			startIndex = j + 1;

		elif(j == len(testSignal) -1):
			filename = str("output/" + testSignal[j]["bot"][0:9]+'.json' )
			outputData = open(filename, 'w')
			print(filename)
			dataDict["Signals"] = testSignal[startIndex:j+1];
			json.dump(dataDict, outputData, indent=4)
			startIndex = j + 1;

testSignal = [];
