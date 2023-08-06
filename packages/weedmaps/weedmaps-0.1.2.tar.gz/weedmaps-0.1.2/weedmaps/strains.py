class Strain:
    """Represents a strain.
    Attributes
    -----------
    id: :class:`str`
        The id of the strain.
    name: :class:`str`
        The display name of the strain.
    """

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
