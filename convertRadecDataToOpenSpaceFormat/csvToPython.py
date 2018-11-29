import json
import csv
from collections import defaultdict
columns = defaultdict(list)
name = ""
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

		row['RAUp'] = float(row['RAUp'])
		row['DecUp'] = float(row['DecUp'])
		row['GeoRngUp'] = float(row['GeoRngUp'])
		row['RTLT_Dn'] = float(row['RTLT_Dn'])
		
		name = row["TimeStamp"][0:14]
		for char in name:
			name = name.replace(":","-")

		outputData = open(str("C:/Agnes/OpenSpace/sync/http/dsn_data/1/positioning/MRONEW/" + name)+'.json', 'w')
		del row['TimeStamp']
		json.dump(row,outputData, indent=4)
