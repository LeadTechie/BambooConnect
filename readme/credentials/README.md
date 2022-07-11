# Readme Details

In order for the recon_tools to access Google Drive you need to do two things:
1. Generate a credentials.json file. (see steps below)
2. Convert this to base64 using 'python authentication_support.py'
3. Set the environment variable to this base64 string [see main readme](../../README.md)

### Related Articles
- Official Instructions: Create access credentials - [Google Workspace for Developers](https://developers.google.com/workspace/guides/create-credentials) The official instructions. Up to date but contains a lot of other variations not needed
- Related Blog Post: Check out the first animated screen flow for how to create the credentials.json (This is example is with Ruby slightly outdated as Google has changed the UI) [Link](https://www.twilio.com/blog/2017/03/google-spreadsheets-ruby.html)


### High Level Instructions
- Goto https://console.cloud.google.com/apis/dashboard
- Create Project
- Add Google Sheets and Google Drive access to it
- Create Service Account for project
- Grant Editor Access to the Service
- Create a JSON Access key
- Note the email address for the service account
- Save credentials.json key and store it in the directory on below the project
- Use the 'use the 'python authentication_support.py' to turn it into a base64 encoded string which you can save as an environment variable (see main readme)

- Go into the individual sheet you own and share it with the service’s dedicated email address eg recontoolsaccessprojectmailaccount@recontoolsaccessproject.iam.gserviceaccount.com


### Screenshot Specific Instructions
This shows the exact screenshots and steps I did
![Step 1](credentials-step1.png?raw=true "Step 1")
![Step 2](credentials-step2.png?raw=true "Step 1")
![Step 3](credentials-step3.png?raw=true "Step 1")
![Step 4](credentials-step4.png?raw=true "Step 1")
![Step 5](credentials-step5.png?raw=true "Step 1")
![Step 6](credentials-step6.png?raw=true "Step 1")
![Step 7](credentials-step7.png?raw=true "Step 1")
![Step 8](credentials-step8.png?raw=true "Step 1")
![Step 9](credentials-step9.png?raw=true "Step 1")
![Step 9a](credentials-step9a.png?raw=true "Step 1")
