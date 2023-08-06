from weedmaps import Client


api = Client()  # Initializing the Client

def get_strain_thc_max(strain_name: str):
    strain = api.search_strain(strain_name)
    return strain.thc_max


strain = get_strain_thc_max('pineapple express')
print(strain)
