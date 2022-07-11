import unittest
import os
import json
from connectors.jira_connector import Jira_Connector
import data_translations as dt

class Test_Unit_Jira_Connector(unittest.TestCase):

    def test_connector_init(self):
        os.environ['RECON_TOOLS_JIRA_EMAIL'] = 'leadtechie@gmail.com'
        os.environ['RECON_TOOLS_JIRA_TOKEN'] = 'test_token'
        os.environ['RECON_TOOLS_JIRA_SERVER'] = 'https://leadtechie.atlassian.net'
        jc = Jira_Connector()

        jc.initialse_auth('RECON_TOOLS_JIRA_EMAIL', 'RECON_TOOLS_JIRA_TOKEN')
        self.assertEqual(jc.user, 'leadtechie@gmail.com')
        self.assertEqual(jc.apikey, 'test_token')

    def test_get_jira_components(self):
        jc = Jira_Connector()
        jc.initialse_auth('RECON_TOOLS_JIRA_EMAIL', 'RECON_TOOLS_JIRA_TOKEN')
        self.assertEqual(jc.get_jira_components_url("https://leadtechie.atlassian.net", "TEST"), "https://leadtechie.atlassian.net/rest/api/3/project/TEST/components")


    def test_parse_components(self):
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
        jira_filtered_component_json = [
            [
                "2022-06-27 22:34:09",
                "10000",
                "TestComponent1",
                "<No Owner>",
                "TestComponent1 Description"
            ],
            [
                "2022-06-27 22:34:09",
                "10001",
                "TestComponent2",
                "<No Owner>",
                "TestComponent2 Description"
            ],
            [
                "2022-06-27 22:34:09",
                "10002",
                "TestComponent3",
                "Chris Rowe",
                "TestComponent3 Description"
            ]
        ]
        new_filtered_list = dt.flatten_jira_components(full_jira_component_json, '2022-06-27 22:34:09')
        self.assertEqual(new_filtered_list, jira_filtered_component_json)


if __name__ == '__main__':
    unittest.main()
