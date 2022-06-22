# library modules
from jira import JIRA

user = 'me@here.com'
apikey = 'your0api0key0here'
server = 'https://SITE_NAME.atlassian.net'

options = {
 'server': server
}

jira = JIRA(options, basic_auth=(user,apikey) )

ticket = 'KRP-11697'
issue = jira.issue(ticket)

summary = issue.fields.summary

print('ticket: ', ticket, summary)
Omantha Prasad
