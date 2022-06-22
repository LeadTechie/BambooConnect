# https://stackoverflow.com/questions/24831543/base-64-encode-a-json-variable-in-python

import json
import base64
import os

#Check that the credentials.json file can be taken from Environment variable and decoded
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
