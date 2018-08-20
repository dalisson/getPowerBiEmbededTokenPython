import adal
import requests
import json

AUTHORITY = "https://login.microsoftonline.com/common"
RESOURCE = "https://analysis.windows.net/powerbi/api"
CLIENTID = "ClientIdGoesHere"
USERNAME = "UserNameGoesHere"
PASSWORD = "PasswordHere"

def get_token(authority, resource, username, password, clientid):
    context = adal.AuthenticationContext(
        authority,
        validate_authority=True,
        api_version=None)

    token_response = context.acquire_token_with_username_password(
        resource,
        username,
        password,
        clientid
    )
    return token_response


response = get_token(AUTHORITY, RESOURCE, USERNAME, PASSWORD, CLIENTID)

aad_token = response['accessToken']

headers = {'Authorization': 'Bearer ' + aad_token}
response = requests.get(
        'https://api.powerbi.com/v1.0/myorg/groups', headers=headers)

bi_groups = json.loads(response.text)['value']

groupId = bi_groups[0]['id']

reportId = "789d98a8-e80e-4f4c-899f-44702d582774"



post_data = post_data = \
    """
        {
            "accessLevel": "View"
        }
    """
headers.update({'Content-type': 'application/json'})
response = requests.post('https://api.powerbi.com/v1.0/myorg/groups/' + groupId + \
         '/reports/' + reportId + '/GenerateToken',data = post_data, headers=headers)

embedToken = json.loads(response.text)['token']
print(embedToken)
