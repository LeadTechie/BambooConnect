# py_recon_tools
recon_tools: Tools to support importing, exporting and reconciliation of data from JIRA, GoogleSheets and more..


### Python Environment Manager - Install Conda:  
- Install - [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)  
[https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)  
- Update [https://www.geeksforgeeks.org/set-up-virtual-environment-for-python-using-anaconda/](https://www.geeksforgeeks.org/set-up-virtual-environment-for-python-using-anaconda/)  
- Set version 3.9.12  
- conda create -n python3-9-12 python=3.9.12 anaconda  
- conda activate python3-9-12  

### Install Packages
- pip install -r ./requirements.txt  

### Set Environment Variables for login
export CREDENTIALS_JSON=""  
export RECON_TOOLS_JIRA_TOKEN=  
export RECON_TOOLS_JIRA_SERVER=
export RECON_TOOLS_JIRA_EMAIL=

### Check Environment Variables for login
echo "$RECON_TOOLS_JIRA_TOKEN"  
echo "$RECON_TOOLS_JIRA_EMAIL"  
echo "$RECON_TOOLS_JIRA_SERVER"
echo "$CREDENTIALS_JSON"

### Run unit tests to check working
- python -m unittest
- python poc_script.py


### Running Tests Locally
- python -m unittest discover -s test/ -p 'test_unit*.py'
- python -m unittest discover -s test/ -p 'test_system*.py'
- python -m unittest discover -s test/ -p 'test_unit_quicktest.py'
