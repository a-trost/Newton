from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.file import Storage

CLIENT_ID = '908601132253-nfkf82kcfqib7mcrvm4mcrmlmblp1alb.apps.googleusercontent.com'
CLIENT_SECRET = 'QdMbXpm2hZpKi8QQnecArWCy'

flow = OAuth2WebServerFlow(
          client_id = CLIENT_ID,
          client_secret = CLIENT_SECRET,
          scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
          redirect_uri = 'http://example.com/auth_return'
       )

storage = Storage('creds.data')
credentials = run_flow(flow, storage)
print("access_token: {}".format(credentials.access_token))