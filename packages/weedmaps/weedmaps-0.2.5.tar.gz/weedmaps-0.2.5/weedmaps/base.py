import weedmaps
import typing
import httpx

class Client():
    def __init__(self):
        self.base_url = 'https://api-g.weedmaps.com/wm/v1/strains'
        self.strains = {}

    # def available_strains(self):
    #     """
    #     Returns all available strains on the Weedmaps API

    #     Returns:
    #         load: A list object with strain names
    #     """

    
    def search_strain(self, query: str, page: int = 1, count_per_page: int = 25):
        if not query:
            return ValueError('Missing a required paramter')


        params = {
            'search': query,
            'page': page,
            'page_size': count_per_page
        }

        response = httpx.get(self.base_url, params=params)  # Send the request using httpx.
        if response.status_code != 200:  # Check if the API returns a 200 status code.
            return response.raise_for_status()  # If not raise error.

        _json = response.json()  # Convert response to a JSON object.


        strain_info = []

        for strain in _json['data']:
            self.strains = {
                'name': strain.get('attributes').get('name'),
                'slug': strain.get('attributes').get('slug'),
                'species': strain.get('attributes').get('species'),
                'description': strain.get('attributes').get('description'),
                'genetic_cultivation_description': strain.get('attributes').get('genetic_cultivation_description'),
                'references': strain.get('attributes').get('references'),
                'hero_image_attribution': strain.get('attributes').get('hero_image_attribution'),
                'lab_data_attribution': strain.get('attributes').get('lab_data_attribution'),
                'thc_min': strain.get('attributes').get('thc_min'),
                'thc_max': strain.get('attributes').get('thc_max'),
                'cbd_min': strain.get('attributes').get('cbd_min'),
                'cbd_max': strain.get('attributes').get('cbd_max'),
                'featured_position': strain.get('attributes').get('featured_position'),
                'featured': strain.get('attributes').get('featured'),
                'avatar_image_url': strain.get('attributes').get('avatar_image_url'),
                'hero_image_url': strain.get('attributes').get('hero_image_url'),
                
            }



        s = weedmaps.models.Strain(
           _name = self.strains.get('name'),
           slug = self.strains.get('slug'),
           species = self.strains.get('species'),
           description= self.strains.get('description'),
           genetic_cultivation_description = self.strains.get('genetic_cultivation_description'),
           references = self.strains.get('references'),
           hero_image_attribution = self.strains.get('hero_image_attribution'),
           lab_data_attribution = self.strains.get('lab_data_attribution'),
           thc_min = self.strains.get('thc_min'),
           thc_max = self.strains.get('thc_max'),
           cbd_min = self.strains.get('cbd_min'),
           cbd_max = self.strains.get('cbd_max'),
           featured_position = self.strains.get('featured_position'),
           featured = self.strains.get('featured'),
           avatar_image_url = self.strains.get('avatar_image_url'),
           hero_image_url = self.strains.get('hero_image_url'),
        )
        return s  # Return data as a "Strain" object.

