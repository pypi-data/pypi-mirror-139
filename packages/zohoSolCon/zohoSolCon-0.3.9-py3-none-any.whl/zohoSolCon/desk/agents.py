import requests
import json


def make_header(token, org_id):
    return {
        "orgId": org_id,
        "Authorization": f"Zoho-oauthtoken {token.access}"
    }


def get_agent(token, org_id, agent_id):
    url = f'https://desk.zoho.com/api/v1/agents/{agent_id}'
    headers = make_header(token, org_id)

    response = requests.get(url=url, headers=headers)

    if response.status_code == 401:
        token.generate()
        return get_agent(token, org_id, agent_id)

    else:
        data = json.loads(response.content.decode('utf-8'))
        return token, data


def get_agents(token, org_id, **kwargs):
    url = 'https://desk.zoho.com/api/v1/agents'
    headers = make_header(token, org_id)

    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_agents(token, org_id, **kwargs)

    else:
        content = json.loads(response.content.decode('utf-8'))
        return token, content.get('data')


def get_agent_count(token, org_id, **kwargs):
    url = 'https://deks.zoho.com/api/v1/agents/count'
    headers = make_header(token, org_id)

    response = requests.get(url=url, headers=headers, params=kwargs)

    if response.status_code == 401:
        token.generate()
        return get_agent_count(token, org_id, **kwargs)

    else:
        content = json.loads(respnse.content.decode('utf-8'))
        return token, content.get("count")


