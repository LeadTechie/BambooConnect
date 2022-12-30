import unittest
import os
import json
import support.authentication_support as auth_sup
#import py_recon_tools.jira_connector.Jira_Connector

class Test_Authentication_Support(unittest.TestCase):

    def test_encode_json_file_to_base64(self):
        should_be  = b'eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInJlY29uLXRvb2xzIiwgInByaXZhdGVfa2V5X2lkIjogInRlc3RzZXRzdHMiLCAicHJpdmF0ZV9rZXkiOiAiYXNkZmFzZGZzZGZcbiIsICJjbGllbnRfZW1haWwiOiAidGVzdEBleGFtcGxlLmNvbSIsICJjbGllbnRfaWQiOiAiMzI0MjM0MzMiLCAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLCAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwgImF1dGhfcHJvdmlkZXJfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMiLCAiY2xpZW50X3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vcm9ib3QvdjEvbWV0YWRhdGEveDUwOS9yZWNvbi10b29scy10ZXN0JTQwcmVjb24tdG9vbHMuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20ifQ=='
        self.assertEqual(should_be, auth_sup.encode_json_file_to_base64('test_data/test_credentials.json'))


        json_string = auth_sup.decode_base64_to_string(should_be)
        stud_obj = json.loads(json_string)
        #print(stud_obj)
        #print("The type of object is: ", type(stud_obj))
        self.assertEqual("service_account", stud_obj['type'])
        auth_sup.print_base64_data('test_data/test_credentials.json')

if __name__ == '__main__':
    unittest.main()
