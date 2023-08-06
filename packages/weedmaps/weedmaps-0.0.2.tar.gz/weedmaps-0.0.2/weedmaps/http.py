import httpx


def get(endpoint: str, params=None):
    if endpoint is None:
        raise ValueError('Missing a required parameter')
    if params is None:
        params = {}

    response = httpx.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        response.raise_for_status()
