from . import constants, http
from models import Strain


class Weedmaps:
    def __init__(self):
        self.search_url = constants.strains_search

    def get_strain(self, query: str) -> Strain:
        if not query:
            raise ValueError('Missing a required argument')
        strain = http.get(self.search_url)
        return Strain(**strain)
