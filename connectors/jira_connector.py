# library modules
import os
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

class Jira_Connector:

    def __init__(self):
        self.user = "leadtechie@gmail.com"
        self.apikey = ""
        self.server = ""
        self.project = ""

    #
    def initialse_auth(self, project="TEST"):
        self.user =  os.getenv('RECON_TOOLS_JIRA_EMAIL')
        self.apikey = os.getenv('RECON_TOOLS_JIRA_TOKEN')
        #https://leadtechie.atlassian.net/rest/api/3/project/TEST/components
        self.server = os.getenv('RECON_TOOLS_JIRA_SERVER')
        self.project = project

    def get_jira_components_url(self, server, project):
        return f'{server}/rest/api/3/project/{project}/components'

    def get_jira_components_default_url(self):
        return self.get_jira_components_url(self.server, self.project)

    def get_jira_components(self):
        return self.call_jira_api(self.get_jira_components_default_url())

    def get_jira_components_json(self):
        return json.loads(self.get_jira_components().content)

    #url string in, returns response
    def call_jira_api(self, url):
        auth = HTTPBasicAuth(self.user, self.apikey)

        headers = {
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check"
        }

        response = requests.request(
            "GET",
            url,
            headers = headers,
            auth = auth
            #files = {
            #     "file": ("myfile.txt", open("myfile.txt","rb"), "application-type")
            #}
            )
        #print(response.content)
        return response

    #
    def parse_components_with_datetime_stamp(self):
        return parse_components(components, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Takes the standard JSON from eg  https://leadtechie.atlassian.net/rest/api/3/project/TEST/components
    # and pulls this out to a flat format: id, name, owners, description
    def parse_components(self, components, time_stamp='2022-06-27 22:54:45'):
        results = []
        for component in components:
            results.append( [ time_stamp,
                component["id"],
                component["name"],
                component['lead']['displayName'] if 'lead' in component else "<No Owner>",
                component['description'] if 'description' in component else "<No Description>"
                ])
        return results

    def test_jira_wrapper_access(self, ticket_name):
        options = {
            'server': self.server
        }

        jira = JIRA(options, basic_auth=(self.user,self.apikey))

        ticket = ticket_name
        issue = jira.issue(ticket)

        summary = issue.fields.summary

        #print('ticket: ', ticket, summary)
        return summary
