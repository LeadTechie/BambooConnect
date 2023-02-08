# https://stackoverflow.com/questions/24831543/base-64-encode-a-json-variable-in-python

import json
import base64
import gspread
import os

#Take the credentials.json file and base64 encode it so you can add as key in environment variable and GitHub secret

def decode_credentials_json():
    credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
    credentials_json = json.loads(credentials_string)
    #pretty_json = json.dumps(credentials_json, indent=4)
    #print(pretty_json)
    return credentials_json

def encode_json_file_to_base64(filename='../credentials.json'):
    with open(filename) as jsonfile:
        data = json.load(jsonfile)
        #print(type(data))  #dict
        datastr = json.dumps(data)
        #print(type(datastr)) #str
        #print(datastr)
        #encoded = base64.b64encode(datastr.encode('utf-8'))  #1 way
        encoded = base64.b64encode(datastr.encode('ascii'))  #1 way

    return encoded

def print_base64_data(filename='../credentials.json'):
    print()
    print('Base64 Encoded json credentials file')
    print(encode_json_file_to_base64(filename))
    print("COPY THE TEXT between the b' and ' above into the gihhub environemnt variable (CREDENTIALS_JSON)")
    print()
    print()


def decode_base64_to_string(base64in):
    return base64.b64decode(base64in).decode('ascii')

def set_env_variable(name, value):
    os.environ[name] = value #encoded.decode('ascii')

def get_env(name):
    return os.getenv(name)

if __name__ == '__main__':
    print_base64_data()
