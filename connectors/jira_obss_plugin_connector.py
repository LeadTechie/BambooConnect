# library modules
import os
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
from connectors.base_connector import Base_Connector

class Jira_OBSS_Plugin_Connector(Base_Connector):
    def __init__(self):
        self.tisjwt = ""
        self.fullURL = ""
        self.clean_data = self.default_clean_data

    def default_clean_data(self, data_in):
        return data_in

    #
    def initialse_auth(self, tisjwt_env, jira_obss_fullURL_env):
        self.tisjwt =  os.getenv(tisjwt_env)
        self.fullURL = os.getenv(jira_obss_fullURL_env)
        #https://leadtechie.atlassian.net/rest/api/3/project/TEST/components

    def initialse_query(self, query_string, clean_data_in=None):
        self.query_string = query_string
        if clean_data_in != None:
            self.clean_data = clean_data_in

    def request_export(self):
        response = self.call_jira_api(self.fullURL).content
        json_response = json.loads(response);
        print ("")
        print ("")
        print ("response " + json.dumps(json_response, indent=4))
        print ("")
        print ("")
        print (json_response['exports'][0]['exportId'])
        print (json_response['exports'][0]['downloadLink'])
        #print (json_response['exports'][0].exportId)
        #print (json_response.exports[0].downloadLink)
        newURL = json_response['exports'][0]['downloadLink']
        newURL= newURL + "?tisjwt=" + self.tisjwt
        print ("FULL NE URL "+newURL )
        response2 = self.call_jira_api(newURL).content
        json_response2 = json.loads(response2);
        print ("")
        print ("")
        print ("response " + json.dumps(json_response2, indent=4))
        return json_response['exports'][0]['downloadLink']

    def get_clean_data(self):
        return self.clean_data(self.get_raw_data())

    def clean_data():
        return ""



    #url string in, returns response
    def call_jira_api(self, url):
        #auth = HTTPBasicAuth(self.user, self.apikey)
        #print(self.fullURL)
        headers = {
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check"
        }

        response = requests.request(
            "GET",
            url,
            headers = headers
            #,
            #auth = auth
            #files = {
            #     "file": ("myfile.txt", open("myfile.txt","rb"), "application-type")
            #}
            )
        print(response.content)
        return response

    def quicktest(self):
        return "quicktest"

    def set_query_details(self, query_string_in):
        self.query_string = query_string_in

    def get_jira_components_url(self, server, project):
        return f'{server}/rest/api/3/project/{project}/components'
