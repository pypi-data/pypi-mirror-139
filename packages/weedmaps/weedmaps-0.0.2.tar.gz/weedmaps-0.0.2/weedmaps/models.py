class Strain:
    strain_id: int
    strain_type: str

    def __init__(self, strain_id: int,
                 strain_type: str):
        self.id = strain_id
        self.type = strain_type
