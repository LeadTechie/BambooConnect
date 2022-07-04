import unittest
import os
import json
from connectors.jira_connector import Jira_Connector
#import py_recon_tools.jira_connector.Jira_Connector

class Test_System_Jira_Connector(unittest.TestCase):
    def test_get_components_from_jira(self):
        jc = Jira_Connector()
        full_jira_component_json = [
            {
                "self": "https://leadtechie.atlassian.net/rest/api/3/component/10000",
                "id": "10000",
                "name": "TestComponent1",
                "description": "TestComponent1 Description",
                "assigneeType": "PROJECT_DEFAULT",
                "realAssigneeType": "PROJECT_DEFAULT",
                "isAssigneeTypeValid": False,
                "project": "TEST",
                "projectId": 10000
            },
            {
                "self": "https://leadtechie.atlassian.net/rest/api/3/component/10001",
                "id": "10001",
                "name": "TestComponent2",
                "description": "TestComponent2 Description",
                "assigneeType": "PROJECT_DEFAULT",
                "realAssigneeType": "PROJECT_DEFAULT",
                "isAssigneeTypeValid": False,
                "project": "TEST",
                "projectId": 10000
            },
            {
                "self": "https://leadtechie.atlassian.net/rest/api/3/component/10002",
                "id": "10002",
                "name": "TestComponent3",
                "description": "TestComponent3 Description",
                "lead": {
                    "self": "https://leadtechie.atlassian.net/rest/api/3/user?accountId=6030eaf45b63c4006822a643",
                    "accountId": "6030eaf45b63c4006822a643",
                    "avatarUrls": {
                        "48x48": "https://secure.gravatar.com/avatar/a2380ea340c13bbc22ba7e607b7aa460?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FCR-3.png",
                        "24x24": "https://secure.gravatar.com/avatar/a2380ea340c13bbc22ba7e607b7aa460?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FCR-3.png",
                        "16x16": "https://secure.gravatar.com/avatar/a2380ea340c13bbc22ba7e607b7aa460?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FCR-3.png",
                        "32x32": "https://secure.gravatar.com/avatar/a2380ea340c13bbc22ba7e607b7aa460?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FCR-3.png"
                    },
                    "displayName": "Chris Rowe",
                    "active": True
                },
                "assigneeType": "PROJECT_DEFAULT",
                "realAssigneeType": "PROJECT_DEFAULT",
                "isAssigneeTypeValid": False,
                "project": "TEST",
                "projectId": 10000
            }
        ]
        os.environ['RECON_TOOLS_JIRA_EMAIL'] = 'leadtechie@gmail.com'
        os.environ['RECON_TOOLS_JIRA_SERVER'] = 'https://leadtechie.atlassian.net'
        jc.initialse_auth()
        full_components_from_jira = jc.get_raw_data()

        #print(full_components_from_jira)
        #new_filtered_list = jc.parse_components(full_components_from_jira, '2022-06-27 22:34:09')
        self.assertEqual(full_components_from_jira, full_jira_component_json)

    def test_test_jira_wrapper_access(self):
        jc = Jira_Connector()
        jc.initialse_auth()
        ticket_description = jc.test_jira_wrapper_access("TEST-3")
        self.assertEqual(ticket_description, "Test Bug 2")


if __name__ == '__main__':
    unittest.main()
