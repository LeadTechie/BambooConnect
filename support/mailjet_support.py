

import requests
import base64
import os

api_key = os.environ['MAILJET_API_KEY']
api_secret = os.environ['MAILJET_API_SECRET']

url = 'https://api.mailjet.com/v3.1/send'

# Load the PDF file and encode it in Base64
with open(os.path.join(os.path.dirname(__file__), 'sample.pdf'), 'rb') as file:
    pdf_data = file.read()
    pdf_encoded = base64.b64encode(pdf_data).decode('utf-8')

# Create the email message
data = {
    'Messages': [
        {
            'From': {
                'Email': '',
                'Name': ''
            },
            'To': [
                {
                    'Email': '',
                    'Name': ''
                }
            ],
            'Subject': 'Test email with attachment',
            'TextPart': 'Hello, world!',
            'Attachments': [
                {
                    'ContentType': 'application/pdf',
                    'Filename': 'sample.pdf',
                    'Base64Content': pdf_encoded
                }
            ]
        }
    ]
}

# Send the email via the Mailjet API
response = requests.post(url, auth=(api_key, api_secret), json=data)

if response.status_code == 200:
    print('Email sent successfully!')
else:
    print('Error sending email:', response.content)
