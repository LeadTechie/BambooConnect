# https://stackoverflow.com/questions/24831543/base-64-encode-a-json-variable-in-python

import json
import base64
import gspread
import os

#Take the credentials.json file and base64 encode it so you can add as key in environment variable and GitHub secret
with open('../credentials.json') as jsonfile:
    data = json.load(jsonfile)
    #print(type(data))  #dict
    datastr = json.dumps(data)
    #print(type(datastr)) #str
    print(datastr)
    #encoded = base64.b64encode(datastr.encode('utf-8'))  #1 way
    encoded = base64.b64encode(datastr.encode('ascii'))  #1 way
    print()
    print('Base64 Encoded json credentials file')
    print(encoded)
    print("COPY THE TEXT between the b' and ' above into the gihhub environemnt variable'")
    print()
    print()

    print('Decode Back to ensure looks OK')
    print()
    print(base64.b64decode(encoded).decode('ascii'))
    print()

stringIn = os.getenv('CREDENTIALS_JSON')
print()
print("CREDENTIALS_JSON as encode('ascii')")
print()
print(stringIn.encode('ascii'))
print()

print()
print('CREDENTIALS_JSON as string')
print()
print(stringIn)
print()

print('CREDENTIALS_JSON decoded')
print()
print(base64.b64decode(stringIn).decode('ascii'))
print()
