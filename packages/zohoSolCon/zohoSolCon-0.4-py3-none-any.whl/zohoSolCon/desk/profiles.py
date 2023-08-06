import requests
import json


def make_header(token, org_id):
    return {
        'orgId': org_id,
        'Authorization': f'Zoho-oauthtoken {token.access}'
    }


def get_profiles(token, org_id, **kwargs):
    url = 'https://desk.zoho.com/api/v1/profiles'
    headers = make_header(token, org_id)

    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_profiles(token, org_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))

        return token, content.get("data")


def get_profile_count(token, org_id, **kwargs):
    
