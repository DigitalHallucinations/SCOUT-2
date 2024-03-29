# modules\Persona\MEDIC JR\Toolbox\maps.py

from modules.Time.time import get_current_info
from modules.Tools.Medical_Tools.PubMedCentral.ENTREZ_API import search_pubmed
from modules.Tools.Medical_Tools.PubMedCentral.PMC_API import search_pmc
from modules.Tools.Base_Tools.Google_search import GoogleSearch


# Create an instance of GoogleSearch
google_search_instance = GoogleSearch()

# A dictionary to map function names to actual function objects
function_map = {
    "get_current_info": get_current_info,
    "google_search": google_search_instance._search,
    "search_pubmed": search_pubmed,
    "search_pmc": search_pmc
}