# library modules
import os
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

user =  os.getenv('RECON_TOOLS_JIRA_EMAIL')
apikey = os.getenv('RECON_TOOLS_JIRA_TOKEN')
#https://leadtechie.atlassian.net/rest/api/3/project/TEST/components
server = os.getenv('RECON_TOOLS_JIRA_SERVER')

#https://community.atlassian.com/t5/Jira-questions/How-to-use-API-token-for-REST-calls-in-Python/qaq-p/760940
#https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
#https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments/#api-rest-api-3-issue-issueidorkey-attachments-post
def testJIRAaccess1():
    options = {
     'server': server
    }

    jira = JIRA(options, basic_auth=(user,apikey) )

    ticket = 'TEST-3'
    issue = jira.issue(ticket)

    summary = issue.fields.summary

    print('ticket: ', ticket, summary)
    return summary

def testJIRAaccess2():
    url = "https://leadtechie.atlassian.net/rest/api/3/project/TEST/components"

    auth = HTTPBasicAuth(user, apikey)

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
    return response

def parseComponentsJSON(components):
    results = []
    for component in components:
        if 'lead' in component:
            lead = component['lead']['displayName']
        else:
            lead = "<No Owner>"
        # Ruby syntax is nicer! hash['description']?hash['description']:'<No Description>'
        if 'description' in component:
            description = component['description']
        else:
            description = "<No Description>",

        results.append( [ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            component["id"],
            component["name"],
            lead,
            description
            ])
    return results

print()
print("RESPONSE")
components = json.loads(testJIRAaccess2().content)
print(json.dumps(parseComponentsJSON(components), indent=4))
print("RESPONSE-END")
