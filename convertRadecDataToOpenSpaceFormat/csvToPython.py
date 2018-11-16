import json
import csv
from collections import defaultdict

columns = defaultdict(list)

with open('data/VGR1-5years.dat') as f:
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
		del row['DLT']
		del row['OneWayDop']
		del row['TwoWayDop']

		row['RADn'] = float(row['RADn'])
		row['DecDn'] = float(row['DecDn'])
		row['GeoRngDn'] = float(row['GeoRngDn'])
		row['RTLT_Dn'] = float(row['RTLT_Dn'])
		
		outputData = open(str("parsed/" + row["TimeStamp"][0:11])+'.json', 'w')
		del row['TimeStamp']
		json.dump(row,outputData, indent=4)
