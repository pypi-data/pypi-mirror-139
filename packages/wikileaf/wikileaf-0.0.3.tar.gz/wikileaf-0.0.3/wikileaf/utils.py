from .models import Strain

import requests

def get_strain(endpoint: str, query: str):
    strains = {}
    response = requests.get(endpoint, params={'type': 'S', 'query': query, 'num': 1})
    if response.status_code != 200:
        return response.raise_for_status()
    else:
        for result in response.json()['results']:
            strains = result
        return strains


def http_to_strain(**kwargs):
    # response = kwargs['response']

    d = get_strain('https://api.wikileaf.com/api/v7/search/all', 'Sour Bubble')
    return Strain(
        score = d.get('score'),
        name = d.get('name'),
        slug = d.get('slug'),
        review_avg = d.get('review_avg'),
        review_count = d.get('review_count'),
        strain_type = d.get('strain_type'),
        consumption_time = d.get('consumption_time'),
        thc_min = d.get('thc_min'),
        thc_max = d.get('thc_max'),
        cbd_min = d.get('cbd_min'),
        cbd_max = d.get('cbd_max'),
        uses = d.get('uses'),
        effects = d.get('effects'),
        logo_url = d.get('logo_url'),
        strain_id = d.get('strain_id'),

    )




