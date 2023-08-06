from models import Strain
from constants import SEARCH_STRAINS
from requests import get


def get_strain(query: str) -> Strain:
    if not query:
        raise ValueError('Missing a required argument')
    response = get(SEARCH_STRAINS)
    strain = response.json()
    return Strain(**strain)
