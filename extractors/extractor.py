# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---



import time
import json
import os
import logging
import requests
import unittest









class Base_Extractor():
    cache_dir=""
    extract = ""
    extract_status_code = 0

    def __init__(self, cache_dir=""):
        self.cache_dir=cache_dir
        None


    #def extract(self, *argv):
    #    None

    def save_results_as_file(self, key_name):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        file_path = os.path.join(self.cache_dir, key_name)
        with open(file_path, "w") as file:
            file.write(self.extract)

    def load_results_from_file(self, key_name):
        file_path = os.path.join(self.cache_dir, key_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                self.extract = file.read()
                self.extract_status_code = 1
                return True
        else:
            return False

    def set_query_details(self, *argv):
        None



# +
def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start} seconds")
        return result
    return wrapper

@measure_time
def my_function():
    # Function implementation here
    time.sleep(2)

#my_function()
# -



class Request_Extractor(Base_Extractor):
    headers = {}
    data = {}
    url = "https://jsonplaceholder.typicode.com/todos/1"
    post_type="GET"
    auth = None

    response = None

    def __init__(self, request_parameters, cache_dir=""):
        super().__init__(cache_dir=cache_dir)
        self.load_request_parameters(request_parameters)
        logging.debug("Request_Connector")

    def load_request_parameters(self, request_parameters):
        self.headers = request_parameters['headers'] if "headers" in request_parameters else {}
        self.data = request_parameters['data'] if "data" in request_parameters else {}
        self.url = request_parameters['url'] if "url" in request_parameters else "https://jsonplaceholder.typicode.com/todos/1"
        self.post_type=request_parameters['post_type'] if "url" in request_parameters else "GET"
        self.auth=request_parameters['auth'] if "auth" in request_parameters else None

    @measure_time
    def extract_data(self, cache_key=""):
        logging.debug("0")
        if self.extract_status_code == 0:
            logging.debug("1")
            if self.load_results_from_file(cache_key):
                logging.debug("2")
                logging.debug(self.extract)
                return self.extract
            else:
                temp_status = self.extract_from_web()
                if cache_key != "":
                    self.save_results_as_file(cache_key)
                logging.debug("3 "+ str(temp_status))
        logging.debug(self.extract)
        logging.debug(type(self.extract))
        return self.extract

    def get_response_status_code(self):
        return self.extract_status_code

    def extract_from_web(self):
        response = requests.request(self.post_type, self.url, headers=self.headers, auth=self.auth, data=self.data)
        self.extract_status_code = response.status_code
        self.extract = response.content.decode()
        logging.debug("extract_from_web" + self.extract)
        return self.extract_status_code








def generate_params_for_jira_component_list(email, token):
    request_params = {}
    request_params['headers'] = {}
    request_params['data'] = {}
    request_params['url'] = "https://leadtechie.atlassian.net/rest/api/3/project/TEST/components"
    request_params['post_type']="GET"
    request_params['auth'] = (email, token)
    request_params['headers'] =  {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    return request_params





#logging.basicConfig(level=logging.ERROR)


# +
class Test_Request_Extractor(unittest.TestCase):

    def test_placeholder_api_test(self):
        expected = {
          "userId": 1,
          "id": 1,
          "title": "delectus aut autem",
          "completed": False
        }

        rc = Request_Extractor({},"./test_data/")
        re = rc.extract_data("")
        re_json = json.loads(re)
        self.assertEqual(re_json, expected, "check json from placeholder external api")

        re = rc.extract_data("jsonplaceholder.json")
        re_json = json.loads(re)
        self.assertEqual(re_json, expected, "check json from external and cache result")

        re = rc.extract_data("jsonplaceholder.json")
        re_json = json.loads(re)
        self.assertEqual(re_json, expected, "check getting from in memory cache")

        Request_Extractor({},"./test_data/")
        re = rc.extract_data("jsonplaceholder.json")
        re_json = json.loads(re)
        self.assertEqual(re_json, expected, "check getting from in file cache")


#logging.basicConfig(level=logging.ERROR)

#unittest.main(argv=[''], verbosity=2, exit=False)
# -



# +


def test_repeated_calls_to_check_cache():
    jira_token = os.environ['JIRA_TOKEN']
    jira_email = os.environ['JIRA_EMAIL']
    request_params = generate_params_for_jira_component_list(jira_email, jira_token)

    re_components = Request_Extractor(request_params, cache_dir="./test_data/")
    components_string = re_components.extract_data("")
    components_json = json.loads(components_string)
    pretty_json = json.dumps(components_json, indent=4)
    #print(pretty_json)

    re_components = Request_Extractor(request_params, cache_dir="./test_data/")
    components_string = re_components.extract_data("")
    components_json = json.loads(components_string)
    pretty_json = json.dumps(components_json, indent=4)
    #print(pretty_json)

    re_components = Request_Extractor(request_params, cache_dir="./test_data/")
    components_string = re_components.extract_data("component_list.json")
    components_json = json.loads(components_string)
    pretty_json = json.dumps(components_json, indent=4)
    #print(pretty_json)

    re_components = Request_Extractor(request_params, cache_dir="./test_data/")
    components_string = re_components.extract_data("component_list.json")
    components_json = json.loads(components_string)
    pretty_json = json.dumps(components_json, indent=4)
    #print(pretty_json)

    components_string = re_components.extract_data("component_list.json")
    components_json = json.loads(components_string)
    pretty_json = json.dumps(components_json, indent=4)
    print(pretty_json)

#test_repeated_calls_to_check_cache()
# -







# +

def flatten_jira_components_with_datetime_stamp(component_json):
    return flatten_jira_components(component_json, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Takes the standard JSON from eg  https://leadtechie.atlassian.net/rest/api/3/project/TEST/components
# and pulls this out to a flat format: time_stampe, id, name, owners, description
def flatten_jira_components(component_json, time_stamp='2022-06-27 22:54:45'):
    results = []
    for component in component_json:
        results.append( [ time_stamp,
            component["id"],
            component["name"],
            component['lead']['displayName'] if 'lead' in component else "<No Owner>",
            component['description'] if 'description' in component else "<No Description>"
            ])
    return results
# -







# +
class Test_Extract_Component_List(unittest.TestCase):

    def test_component_list(self):
        expected = {
            "self": "https://leadtechie.atlassian.net/rest/api/3/component/10000",
            "id": "10000",
            "name": "TestComponent1",
            "description": "TestComponent1 Description",
            "assigneeType": "PROJECT_DEFAULT",
            "realAssigneeType": "PROJECT_DEFAULT",
            "isAssigneeTypeValid": False,
            "project": "TEST",
            "projectId": 10000
        }

        jira_token = os.environ['JIRA_TOKEN']
        jira_email = os.environ['JIRA_EMAIL']
        request_params = generate_params_for_jira_component_list(jira_email, jira_token)

        re_components = Request_Extractor(request_params, cache_dir="./test_data/")
        components_string = re_components.extract_data("")
        re_components_json = json.loads(components_string)

        pretty_json = json.dumps(re_components_json, indent=4)
        self.assertEqual(re_components_json[0], expected, "check first component")

# +

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
# -

# from transform.recon_dataset import Recon_DataSet
# from transform import data_translations
