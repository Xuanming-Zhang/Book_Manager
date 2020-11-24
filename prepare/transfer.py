import csv
import json

csvfile = open('books.csv', 'r',encoding='utf8')
jsonfile = open('books.json', 'w')


reader = csv.DictReader(csvfile)
jsonfile.write('[')

for i,row in enumerate(reader):
    json.dump(row, jsonfile)
    jsonfile.write(',')
    jsonfile.write('\n')

csvfile.close()
jsonfile.close()
