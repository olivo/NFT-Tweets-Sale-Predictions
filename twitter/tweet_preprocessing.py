from operator import neg
import ast
import os
import requests
from requests.structures import CaseInsensitiveDict
import json
import time

def preprocess_directory(inputDirectory, outputFile):
    outputStream = open(outputFile, "w", encoding='ascii')
    outputStream.write("id,author_id,created_at,text\n")
        
    for filename in os.listdir(inputDirectory):
        f = os.path.join(inputDirectory, filename)
        
        if os.path.isfile(f):
            #print("File: " + f)
            inputStream = open(f, "r", encoding='utf-8')
            fileContents = inputStream.read()
            
            json_data = ast.literal_eval(fileContents)
            
            for elem in json_data:
                text = "\""+elem['text'].encode('ascii', 'ignore').decode('ascii').replace("\n", "").replace("\"", "'")+"\""
                outputStream.write(elem['id']+","+elem['author_id']+","+elem['created_at']+","+text+"\n")
            
            #fileContents = fileContents.strip("'<>() ").replace('\'', '\"')

            #outputStream.write(fileContents.encode('ascii', 'ignore').decode('ascii'))

            #f2 = open(outputFile, "r", encoding="ascii")
            #jsonContents = json.loads(f2.read())


            
            #jsonContents = json.load(inputStream)
            #jsonContents = json.loads(json.dumps(fileContents))

            #jsonContents = jsonContents.replace("'created_at'", "\"created_at\"")
            #jsonContents = jsonContents.replace("'id'", "\"id\"")
            #jsonContents = jsonContents.replace("'author_id'", "\"author_id\"")
            #jsonContents = jsonContents.replace("'text'", "\"text\"")
            #jsonContents = jsonContents.replace("\'", "\"")

            #fileContents = fileContents.encode('ascii', 'ignore').decode('ascii')
            #json_data = ast.literal_eval(json.dumps(fileContents))
            #json_data = json_data.replace("'", "\"")

            #print(json_data)

            #print(jsonContents)
            #print(type(json_data))

            #convertedContent = json.loads(json_data)
            #print(type(convertedContent))
            #print(type(json.load(jsonContents)))
            #for jsonEntry in jsonContents:
            #    print(jsonEntry)
            #    return 0

            #print(jsonContents)

preprocess_directory(inputDirectory = "data/raw/coolcats/07-10_2021", outputFile = "data/preprocessed/coolcats_07-10_2021.csv")