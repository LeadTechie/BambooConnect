# library modules
import os
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
from connectors.base_connector import Base_Connector

class Jira_Connector(Base_Connector):
    def __init__(self):
        self.user = ""
        self.apikey = ""
        self.query_string = ""
        self.clean_data = self.default_clean_data

    def default_clean_data(self, data_in):
        return data_in

    #
    def initialse_auth(self, user_env, apikey_env):
        self.user =  os.getenv(user_env)
        self.apikey = os.getenv(apikey_env)
        #https://leadtechie.atlassian.net/rest/api/3/project/TEST/components

    def initialse_query(self, query_string, clean_data_in=None):
        self.query_string = query_string #self.get_jira_components_url(self.server, self.project)
        if clean_data_in != None:
            self.clean_data = clean_data_in

    def get_raw_data(self):
        return json.loads(self.call_jira_api().content);

    def get_clean_data(self):
        return self.clean_data(self.get_raw_data())

    def clean_data():
        return ""





    #url string in, returns response
    def call_jira_api(self):
        auth = HTTPBasicAuth(self.user, self.apikey)

        headers = {
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check"
        }

        response = requests.request(
            "GET",
            self.query_string,
            headers = headers,
            auth = auth
            #files = {
            #     "file": ("myfile.txt", open("myfile.txt","rb"), "application-type")
            #}
            )
        #print(response.content)
        return response



    def set_query_details(self, query_string_in):
        self.query_string = query_string_in











# Unused, to be deleted...

    # Another way to access jira through a higher level wrapper
    def test_jira_wrapper_access(self, ticket_name, server_name):
        options = {
            'server': server_name
        }

        jira = JIRA(options, basic_auth=(self.user,self.apikey))

        ticket = ticket_name
        issue = jira.issue(ticket)

        summary = issue.fields.summary

        #print('ticket: ', ticket, summary)
        return summary

    def get_jira_components_url(self, server, project):
        return f'{server}/rest/api/3/project/{project}/components'
