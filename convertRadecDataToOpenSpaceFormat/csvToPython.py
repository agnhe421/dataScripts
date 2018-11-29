import json
import csv
from collections import defaultdict

name = ""
hours = []
names = []
positions = {}
data = []
oneHourData = []


with open('data/MRO-everyminute.dat') as f:
	reader = csv.DictReader(f, fieldnames=['TimeStamp', 'AzUp', 'ElUp', 'RngUp', 'AzDn', 'ElDn', 'RngDn', 
		'RAUp', 'DecUp', 'GeoRngUp', 'RADn', 'DecDn', 'GeoRngDn', 'ULT', 'RTLT_Up', 'XADop', 'DLT', 'RTLT_Dn', 'OneWayDop', 'TwoWayDop']) 
	for row in reader:
		del row['AzUp']
		del row['ElUp']
		del row['RngUp']
		del row['AzDn']
		del row['ElDn']
		del row['RngDn']
		del row['RADn'] 
		del row['DecDn']
		del row['GeoRngDn']
		del row['ULT']
		del row['RTLT_Up']
		del row['XADop']
		del row['DLT']
		del row['OneWayDop']
		del row['TwoWayDop']
		del row['RTLT_Dn']

		row['RAUp'] = float(row['RAUp'])
		row['DecUp'] = float(row['DecUp'])
		row['GeoRngUp'] = float(row['GeoRngUp'])
		row['TimeStamp'] = row['TimeStamp'][0:14]
		
		name = row["TimeStamp"][0:11]
		names.append(name)

		hour = row["TimeStamp"][9:11]
		hours.append(int(hour))

		data.append(row)

for i in range(0, len(hours)):
	if(i+1 < len(hours) and hours[i] == hours[i+1]):
		oneHourData.append(data[i])
	else:
		outputData = open(str("C:/Agnes/OpenSpace/sync/http/dsn_data/1/positioning/MRO/" + names[i])+'.json', 'w')
		positions["Positions"] = oneHourData
		json.dump(positions,outputData, indent=4)
		del oneHourData[:]

