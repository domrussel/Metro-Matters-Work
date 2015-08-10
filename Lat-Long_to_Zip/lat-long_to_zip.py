import csv
import requests
import json




def get_zip(lati, longi):
    d = {'latlng' : '%s,%s' % (lati, longi), 'key' : 'AIzaSyCQvKC7Q1C54YdgJOx6QFxP1aLUmgr7XuQ'}
    geo_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params = d)
    geo_dict = json.loads(geo_json.text)
    for dic in geo_dict['results'][0]['address_components']:
        if dic['types'] == ['postal_code']:
            print dic['long_name']
            return dic['long_name']
    print "ERROR"
    return None

unit_dict = {}     
    
def get_zips_for_csv(read_csv, write_csv, col_numb_1, col_numb_2):
a = open(read_csv)
csv_a = csv.reader(a)
for proj in csv_a:
    lati = proj[col_numb_1]
    longi = proj[col_numb_2]
    if lat == '-1':
        print 'lat = -1'
        pass
    else:
        print lati, longi    
        try:
            zip = get_zip(lati, longi)
        except:
            print 'error'
            pass
        try:
            units = int(proj[10])
        except:
            pass
        if zip in unit_dict:
            unit_dict[zip] += units
        else:
            unit_dict[zip] = units
        
    projwrit = csv.writer(open(write_csv, 'wb'))
    projwrit.writerow(['zip', 'units'])
    for zip in unit_dict:
        projwrit.writerow([zip, unit_dict[zip]])
    
###example call

get_zips_for_csv('mip.csv', 64, 65)
    