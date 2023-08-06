from .utils import get_strain, http_to_strain
from .constants import SEARCH
class Leaf:
    """ The base class for Wikileaf

    """

    def __init__(self):
        """ Initialize Leaf class

        """
        self.name = 'Placeholder'

    def search_strains(self, query: str):
        """ Search for a strain

        Search and return data for a specific strain of
        cannabis

        Args:
            query (str): the strain to search for
        """
        response = get_strain(SEARCH, query)
        return http_to_strain(response=response)
        # return response




