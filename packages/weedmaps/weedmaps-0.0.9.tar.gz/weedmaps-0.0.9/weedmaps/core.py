from models import Strain
from constants import SEARCH_STRAINS
from requests import get


class API:
    def __init__(self):
        self.search_url = SEARCH_STRAINS

    def get_strain(self, query: str) -> Strain:
        if not query:
            raise ValueError('Missing a required argument')
        strain = get(self.search_url)
        return Strain(**strain)
